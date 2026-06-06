from django.shortcuts import render
from django.http import HttpResponseNotFound
from .models import Book
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    try:
        books = Book.objects.all()
        query = request.GET.get("query_search")
        date_start = request.GET.get("start")
        date_end = request.GET.get("end")

        if query:
            books = books.filter(
                Q(title__icontains=query) | Q(author__name__icontains=query)
            )

        if date_start and date_end:
            books = books.filter(publication_date__range=[
                                 date_start, date_end])

        paginator = Paginator(books, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        query_params = request.GET.copy()
        if "page" in query_params:
            query_params.pop("page")
        query_string = query_params.urlencode()

        return render(request, "minilibrary/minilibrary.html", {
            "page_obj": page_obj,
            "query": query,
            "query_string": query_string
        })
    except Exception:
        return HttpResponseNotFound("Página no encontrada")