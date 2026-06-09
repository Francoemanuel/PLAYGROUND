from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="minilibrary"),
    path('recomendar/<int:book_id>/', views.add_review, name="recommend_book"),
    path('hello', views.Hello.as_view(), name="hello_cbv"),
    path('welcome/', views.WelcomeView.as_view(), name="welcome"),
    path('books/', views.BookListView.as_view(), name="book_list"),
    path("books/add", views.add_book, name="add_book"),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name="book_detail"),
    path('books/<int:pk>/review/',
         views.ReviewCreateView.as_view(), name="add_review"),
    path('review/<int:pk>/edit/',
         views.ReviewUpdateView.as_view(), name="edit_review"),
    path('review/<int:pk>/delete/',
         views.ReviewDeleteView.as_view(), name="delete_review"),
    path("time-test/", views.time_test),
    path("counter/", views.visit_counter),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
