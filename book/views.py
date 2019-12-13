from datetime import datetime

from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from accounts.models import Profile
from book.models import BookInfo, Shelf, ProfileBookInfo

DEFAULT_BOOK_IMAGE_URL = "https://previews.123rf.com/images/chupakabrajk/chupakabrajk1811/chupakabrajk181100009/111711652-book-vector-illustration-of-a-textbook-a-book-closed-book-with-the-inscription-book-.jpg"

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

        if apiResponse['totalItems'] == 0:
                apiResponse = []
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
            volume_info = book_info.get('volumeInfo')
            image_link = volume_info.get('imageLinks', {}).get('smallThumbnail', DEFAULT_BOOK_IMAGE_URL)
            book = BookInfo(google_id=id,
                            title=title,
                            authors=(",").join(volume_info.get('authors', 'Unknown author')),
                            description=volume_info.get('description', 'No description'),
                            pageCount=volume_info.get('pageCount', ''),
                            small_pic_url=image_link,
                            )
            book.save()

            shelf_name = request.GET.get('shelf').replace("%20", " ")
            shelf = profile.shelves.get(name=shelf_name)
            # here should be check for book on shelf,
            # actually it had to be before

            profile.books.add(book)
            profile_book_info = ProfileBookInfo()

            profile_book_info.profile = profile
            profile_book_info.shelf = shelf
            profile_book_info.book = book
            profile_book_info.time = datetime.now()
            # #profile=profile, book=book, time=datetime.now()
            # time_added.add(profile=profile)
            #
            profile_book_info.save()
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

    current_shelf = Shelf.objects.get(name=current_shelf_name, profile=request.user.profile)

    shelf_objs = []
    for name in shelf_names:
        shelf_obj = {
            "name": name,
            "active": "active" if name==current_shelf_name else ""
        }
        shelf_objs.append(shelf_obj)

    profile_book_objs = list(current_shelf.profile_books.all())
    books = [profile_book_obj.book for profile_book_obj in profile_book_objs]

    # print('!!!!!!!!!!!!')
    # print(books)
    # print('!!!!!!!!!!!!')

    if books == []:
        return render(request, 'book/book_list.html',
                      {'shelves': shelf_objs,
                       'now': datetime.now()
                       })
    else:
        time = []
        for book in books:
            time_object = ProfileBookInfo.objects.get(book=book, profile=request.user.profile)
            time.append(time_object.time)

        books_with_time = zip(books, time)

        return render(request, 'book/book_list.html',
                      {'shelves': shelf_objs,
                       'books_with_time': books_with_time,
                       'now': datetime.now()
                       })
    # shelves_names = ','.join([shelf.name for shelf in shelves])
    # return HttpResponse(shelves_names)


def delete_book(request):
    try:
        id = request.GET.get('id').replace("%20", " ")
        # shelf = request.GET.get('shelf').replace("%20", " ")
    except AttributeError:
        raise Http404
    profile_book = request.user.profile.books.filter(google_id=id)[0]
    title = profile_book.title
    profile_book.delete()
    messages.success(request, f'Book "{title}" was deleted')
    # _book = request.user.profile.profile_books.get(shelf=shelf, google_id=id)
    # shelf_book.delete()
    return redirect('book_list')


def move_book(request):
    try:
        from_shelf_name = request.GET.get('from').replace("%20", " ")
        to_shelf_name = request.GET.get('to').replace("%20", " ")
        id = request.GET.get('id').replace("%20", " ")
    except AttributeError:
        raise Http404

    try:
        from_shelf_obj = Shelf.objects.filter(name=from_shelf_name, profile=request.user.profile)[0]
        to_shelf_obj = Shelf.objects.filter(name=to_shelf_name, profile=request.user.profile)[0]
        book_obj = BookInfo.objects.filter(google_id=id)[0]
        profile_book_info_obj = ProfileBookInfo.objects.filter(book=book_obj, profile=request.user.profile)[0]
    except:
        raise Http404

    profile_book_info_obj.shelf = to_shelf_obj
    profile_book_info_obj.save()

    messages.success(request, f'Book "{book_obj.title}" was successfully moved from "{from_shelf_name}" to "{to_shelf_name}" shelf')
    return redirect('book_list')