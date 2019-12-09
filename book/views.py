from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from accounts.models import Profile
from book.models import BookInfo


class BookSearch(View):
    def get(self, request):
        profile = get_object_or_404(Profile, pk=request.user.id)
        shelves = list(x.name for x in profile.shelves.all())
        print(shelves)
        apiResponse = None
        queryParam = request.GET.get('query')
        if (queryParam != "" and queryParam is not None):
            query = request.GET['query'].replace(" ","%20")
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
            title = request.GET.get('title').replace("%20"," ")
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

    # @csrf_exempt
    # def post(self, request):
    #     return render(request, 'book/book_search.html', {})
