from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Book, Review
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import ReviewForm
from django.contrib.auth import get_user_model
from django.contrib import messages
# Create your views here.

User = get_user_model()


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


def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            would_recommend = form.cleaned_data.get('would_recommend')
            if would_recommend:
                messages.success(
                    request, "Gracias por la reseña y tu recomendación de nuestros libros")
            else:
                messages.success(request, "Gracias por la reseña")
            return redirect("recommend_book", book_id=book.id)
        else:
            messages.error(
                request, "Corrige los errores del formulario", "danger")

    return render(request, "minilibrary/add_review.html", {
        "form": form,
        "book": book
    })
