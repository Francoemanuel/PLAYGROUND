from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loan
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
User = get_user_model()

admin.site.site_header = "Administrador MiniLibrary"
admin.site.site_title = "Minilibrary panel"
admin.site.index_title = "Bienvenidos al panel de minilibrary"


@admin.action(description="Marcar préstamos como devueltos")
def mark_as_returned(modeladmin, request, queryset):
    queryset.update(is_returned=True)


class LoanInline(admin.TabularInline):
    model = Loan
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


class BookDetailInline(admin.StackedInline):
    model = BookDetail
    can_delete = False
    verbose_name_plural = "Detalle del libro"


class CustomUserAdmin(BaseUserAdmin):
    inlines = [LoanInline]
    list_display = ("username", "email")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, BookDetailInline]
    list_display = ('title', 'author', 'pages', 'publication_date')
    search_fields = ('title', 'author__name')
    list_filter = ('author', 'genres', 'publication_date')
    ordering = ['-publication_date']
    date_hierarchy = 'publication_date'
    autocomplete_fields = ["author", "genres"]

    fieldsets = (
        ("Información general", {
            "fields": ("title", "author", "publication_date", "genres")
        }),
        ("Detalles", {
            "fields": ("isbn", "pages"),
            "classes": ("collapse",)
        }),
    )

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ("loan_date",)
    list_display = ("user", "book", "loan_date", "is_returned")
    actions = [mark_as_returned]
    raw_id_fields = ["user", "book"]


# admin.site.register(Author)
# admin.site.register(Book, BookAdmin)
# admin.site.register(Genre)
admin.site.register(BookDetail)
admin.site.register(Review)
# admin.site.register(Loan)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
