from datetime import datetime

from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.views.generic import RedirectView, DetailView

from accounts.models import Profile
from book.models import BookInfo, Shelf, ProfileBookInfo

DEFAULT_BOOK_IMAGE_URL = "https://previews.123rf.com/images/chupakabrajk/chupakabrajk1811/chupakabrajk181100009/111711652-book-vector-illustration-of-a-textbook-a-book-closed-book-with-the-inscription-book-.jpg"


class BookSearch(View):
    def get(self, request):
        profile = request.user.profile
        # print('11111111')
        # print(profile)
        # print('11111111')
        shelves = list(x.name for x in profile.shelves.all())
        print(shelves)
        queryParam = request.GET.get('query')
        if (queryParam != "" and queryParam is not None):
            query = request.GET['query'].replace(" ", "%20")
            apiResponse = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}').json()
        else:
            return redirect('book_list')

        if apiResponse['totalItems'] == 0:
            apiResponse = []

        if profile.books.all == []:
            profile_books_objs = []
        else:
            profile_books_objs = profile.books.all()
        # print(profile_books_objs)
        profile_books = [profile_books_obj.google_id for profile_books_obj in profile_books_objs]
        print(profile_books)
        # print(apiResponse)
        return render(request, 'book/book_search.html',
                      {'book_list': apiResponse, 'shelves': shelves, 'profile_books': profile_books})


def add_book_to_db(request, id):
    book_info = requests.get(f'https://www.googleapis.com/books/v1/volumes/{id}').json()
    try:
        book = BookInfo.objects.get(google_id=id)
    except BookInfo.DoesNotExist:
        volume_info = book_info.get('volumeInfo')
        image_link = volume_info.get('imageLinks', {}).get('smallThumbnail', DEFAULT_BOOK_IMAGE_URL)
        book = BookInfo(google_id=id,
                        title=volume_info.get('title'),
                        authors=(",").join(volume_info.get('authors', ['Unknown author'])),
                        description=volume_info.get('description', 'No description'),
                        pageCount=volume_info.get('pageCount', ''),
                        small_pic_url=image_link,
                        )
        book.save()
    return redirect('book_detail', id=book.id)


class AddToBookshelf(RedirectView):
    def get(self, request, id):
        profile = Profile.objects.filter(user=request.user)[0]

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
                            authors=(",").join(volume_info.get('authors', ['Unknown author'])),
                            description=volume_info.get('description', 'No description'),
                            pageCount=volume_info.get('pageCount', ''),
                            small_pic_url=image_link,
                            )
            book.save()

        shelf_name = request.GET.get('shelf').replace("%20", " ")
        shelf = profile.shelves.get(name=shelf_name)
        # here should be check for book on shelf,
        # actually it had to be before

        if book not in profile.books.all():
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
        else:
            messages.warning(request, f'Your already have this book on shelf')

        print(profile.bio)
        # return render(request, 'book/book_add.html', {'book': book_info})
        return redirect('book_list')


class BookDetail(View):
    def get(self, request, id):
        if not id:
            raise Http404
        book = get_object_or_404(BookInfo, id=id)
        show_select_field = True
        shelves = list(x.name for x in request.user.profile.shelves.all())
        print(shelves)
        from_shelf = None
        if book in request.user.profile.books.all():
            show_select_field = False
            from_shelf = ProfileBookInfo.objects.get(book=book, profile=request.user.profile).shelf.name
            shelves.remove(from_shelf)


        return render(request, 'book/book_detail.html', {'book': book, 'show_select_field': show_select_field, 'shelves': shelves, 'from_shelf': from_shelf})


def show_books(request):
    shelves = Shelf.objects.filter(profile=request.user.profile)
    tags = request.user.profile.tags.all()
    # if tags == book.tag.None:
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
            "active": "active" if name == current_shelf_name else ""
        }
        shelf_objs.append(shelf_obj)

    profile_book_objs = list(current_shelf.profile_books.all().order_by('-time'))
    profile_books = [profile_book_obj for profile_book_obj in profile_book_objs]

    return render(request, 'book/book_list_ajax.html',
                  {'shelves': shelf_objs,
                   'profile_books': profile_books,
                   'tags': tags,
                   })


def show_books_by_tag(request, tag_name):
    tag_names = [tag.name for tag in request.user.profile.tags.all()]
    if tag_name not in tag_names:
        raise Http404
    profile_books = list(ProfileBookInfo.objects.filter(profile=request.user.profile, tags__name__exact=tag_name).order_by('-time'))
    # books = [profile_book for profile_book in profile_books]
    # print(books)
    # books = [profile_book_obj.book for profile_book_obj in profile_book_objs]

    return render(request, 'book/book_list_tag.html',
                  {'profile_books': profile_books,
                   'current_tag': tag_name,
                   'tags': tag_names,
                   })
    # return render(request, 'book/book_list.html',
    #               {'books_with_info': books_with_info,
    #                'tags': tags,
    #                })


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
    profile_book_info_obj.time = datetime.now()
    profile_book_info_obj.save()

    messages.success(request,
                     f'Book "{book_obj.title}" was successfully moved from "{from_shelf_name}" to "{to_shelf_name}" shelf')
    return redirect('book_list')


class AddTagToBook(View):
    def get(self, request):

        id1 = request.GET.get('id', None)

        tags1 = request.GET.getlist('tag', None)
        print("!!!!!!!")
        print(tags1)
        print("!!!!!!!")

        profile_book_info = ProfileBookInfo.objects.get(id=id1, profile=request.user.profile)
        current_shelf = profile_book_info.shelf.name.replace(" ", "%20")
        if (tags1):
            for tagName in tags1:
                tagObj = request.user.profile.tags.get(name=tagName)
                profile_book_info.tags.add(tagObj)
            profile_book_info.save()
            messages.success(request, f'You\'ve added some tags for "{profile_book_info.book.title}" book')
        else:
            messages.warning(request, f'No tags were added for "{profile_book_info.book.title}" book')

        return redirect(reverse('book_list')+f'?shelf={current_shelf}')


class AddTagToBookAjax(View):
    def get(self, request):

        id1 = request.GET.get('id', None)

        tags1 = request.GET.getlist('tag[]', None)
        print("!!!!!!!")
        print(tags1)
        print("!!!!!!!")

        profile_book_info = ProfileBookInfo.objects.get(id=id1, profile=request.user.profile)
        if (tags1):
            for tagName in tags1:
                tagObj = request.user.profile.tags.get(name=tagName)
                profile_book_info.tags.add(tagObj)
            profile_book_info.save()
            data = {
                'tag': tags1,
                'bookId': id1
            }
        else:
            data = {'err': 'error occured'}

        return JsonResponse(data)


class DeleteTagFromBookAjax(View):
    def get(self, request):
        bookId = request.GET.get('bookId', None)
        tagName = request.GET.get('tagName', None)

        profile_book_info = ProfileBookInfo.objects.get(id=bookId, profile=request.user.profile)
        if (tagName and bookId):
            tagObj = request.user.profile.tags.get(name=tagName)
            profile_book_info.tags.remove(tagObj)
            profile_book_info.save()

            data = {
                'bookId': bookId,
                'tagName': tagName
            }
        else:
            data = {'err': 'error occured'}
        return JsonResponse(data)