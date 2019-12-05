from django.shortcuts import render
from django.views import View
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class BookSearch(View):
    def get(self, request):
        apiResponse = None
        queryParam = request.GET.get('query')
        if (queryParam != "" and queryParam is not None):
            query = request.GET['query'].replace(" ","%20")
            apiResponse = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}').json()
            print(apiResponse)
        return render(request, 'book/book_search.html', {'book_list': apiResponse})

    # @csrf_exempt
    # def post(self, request):
    #     return render(request, 'book/book_search.html', {})
