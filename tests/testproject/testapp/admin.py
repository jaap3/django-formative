from django.contrib import admin
from formative.admin import InlineFormativeBlobAdmin, FormativeBlobInline
from tests.testproject.testapp.models import Book


class BookAdmin(InlineFormativeBlobAdmin):
    inlines = [FormativeBlobInline]


admin.site.register(Book, BookAdmin)
