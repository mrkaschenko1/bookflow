from django.shortcuts import render, redirect
from django.views import View
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from accounts.models import Profile


class BookSearch(View):
    def get(self, request):
        apiResponse = None
        queryParam = request.GET.get('query')
        if (queryParam != "" and queryParam is not None):
            query = request.GET['query'].replace(" ","%20")
            apiResponse = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}').json()
            print(apiResponse)
        return render(request, 'book/book_search.html', {'book_list': apiResponse})


class AddToBookshelf(View):
    def get(self, request, id):
        current_user_id = request.user.id
        profile = Profile.objects.get(current_user_id)
        print(profile.bio)
        return redirect('home')

    # @csrf_exempt
    # def post(self, request):
    #     return render(request, 'book/book_search.html', {})
