from django.contrib import admin
from formative.admin import InlineFormativeBlobAdmin, FormativeBlobInline
from tests.testproject.testapp.models import Book


class CustomFormativeBlobInline(FormativeBlobInline):
    extra = 1


class BookAdmin(InlineFormativeBlobAdmin):
    inlines = [CustomFormativeBlobInline]


admin.site.register(Book, BookAdmin)
