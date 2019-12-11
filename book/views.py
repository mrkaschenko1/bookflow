from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from accounts.models import Profile
from book.models import BookInfo, Shelf


class BookSearch(View):
    def get(self, request):
        profile = get_object_or_404(Profile, pk=request.user.id)
        shelves = list(x.name for x in profile.shelves.all())
        print(shelves)
        apiResponse = None
        queryParam = request.GET.get('query')
        if (queryParam != "" and queryParam is not None):
            query = request.GET['query'].replace(" ", "%20")
            apiResponse = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}').json()
            # print(apiResponse)
        return render(request, 'book/book_search.html', {'book_list': apiResponse, 'shelves': shelves})


class AddToBookshelf(View):
    def get(self, request, id):
        profile = get_object_or_404(Profile, pk=request.user.id)

        book_info = requests.get(f'https://www.googleapis.com/books/v1/volumes/{id}').json()

        print(id)

        try:
            book = BookInfo.objects.get(google_id=id)
        except BookInfo.DoesNotExist:
            title = request.GET.get('title').replace("%20", " ")
            book = BookInfo(google_id=id,
                            title=title,
                            authors=(",").join(book_info['volumeInfo']['authors']),
                            description=book_info['volumeInfo']['description'],
                            pageCount=book_info['volumeInfo']['pageCount'],
                            small_pic_url=book_info['volumeInfo']['imageLinks']['smallThumbnail'],
                            )
            book.save()

            shelf_name = request.GET.get('shelf').replace("%20", " ")
            shelf = profile.shelves.get(name=shelf_name)
            # here should be check for book on shelf,
            # actually it had to be before
            shelf.books.add(book)
            messages.success(request, f'Your book was added on {shelf_name} shelf!')

        print(profile.bio)
        return render(request, 'book/book_add.html', {'book': book_info})

# def get_active_shelf(name, current):
#     return  "active" ? name == current : ""

def show_books(request):
    shelves = Shelf.objects.filter(profile=request.user.profile)
    shelf_names = [shelf.name for shelf in shelves]
    try:
        current_shelf_name = request.GET.get('shelf').replace("%20", " ")
    except AttributeError:
        current_shelf_name = 'To read'
    if current_shelf_name not in shelf_names:
        raise Http404

    shelf_objs = []
    for name in shelf_names:
        shelf_obj = {
            "name": name,
            "active": "active" if name==current_shelf_name else ""
        }
        shelf_objs.append(shelf_obj)

    books = list(Shelf.objects.filter(name=current_shelf_name, profile=request.user.profile)\
                                .first().books.all())
    return render(request, 'book/book_list.html',
                  {'shelves': shelf_objs,
                   'books': books
                   })
    # shelves_names = ','.join([shelf.name for shelf in shelves])
    # return HttpResponse(shelves_names)
