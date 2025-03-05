from ninja import NinjaAPI, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404
from ninja.security import django_auth
from catalog.models import Author, Genre, Language, Book, BookInstance

api = NinjaAPI(auth=django_auth)

# Schemas
class AuthorSchema(Schema):
    id: int
    first_name: str
    last_name: str
    date_of_birth: Optional[str] = None
    date_of_death: Optional[str] = None

class AuthorCreateSchema(Schema):
    first_name: str
    last_name: str
    date_of_birth: Optional[str] = None
    date_of_death: Optional[str] = None

class GenreSchema(Schema):
    id: int
    name: str

class GenreCreateSchema(Schema):
    name: str

class LanguageSchema(Schema):
    id: int
    name: str

class LanguageCreateSchema(Schema):
    name: str

class BookSchema(Schema):
    id: int
    title: str
    author: AuthorSchema
    summary: str
    isbn: str
    genre: List[GenreSchema]
    language: LanguageSchema

class BookCreateSchema(Schema):
    title: str
    author_id: int
    summary: str
    isbn: str
    genre_ids: List[int]
    language_id: int

class BookInstanceSchema(Schema):
    id: int
    book: BookSchema
    imprint: str
    status: str
    due_back: Optional[str]

class BookInstanceCreateSchema(Schema):
    book_id: int
    imprint: str
    status: str
    due_back: Optional[str]

# Author Endpoints
@api.get("/authors", response=List[AuthorSchema])
def list_authors(request):
    return Author.objects.all()

@api.get("/authors/{author_id}", response=AuthorSchema)
def get_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    return author

@api.post("/authors", response=AuthorSchema, auth=django_auth)
def create_author(request, payload: AuthorCreateSchema):
    author = Author.objects.create(**payload.dict())
    return author

@api.put("/authors/{author_id}", response=AuthorSchema, auth=django_auth)
def update_author(request, author_id: int, payload: AuthorCreateSchema):
    author = get_object_or_404(Author, id=author_id)
    for attr, value in payload.dict().items():
        setattr(author, attr, value)
    author.save()
    return author

@api.delete("/authors/{author_id}", auth=django_auth)
def delete_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return {"success": True}

# Genre Endpoints
@api.get("/genres", response=List[GenreSchema])
def list_genres(request):
    return Genre.objects.all()

@api.post("/genres", response=GenreSchema, auth=django_auth)
def create_genre(request, payload: GenreCreateSchema):
    genre = Genre.objects.create(**payload.dict())
    return genre

@api.delete("/genres/{genre_id}", auth=django_auth)
def delete_genre(request, genre_id: int):
    genre = get_object_or_404(Genre, id=genre_id)
    genre.delete()
    return {"success": True}

# Language Endpoints
@api.get("/languages", response=List[LanguageSchema])
def list_languages(request):
    return Language.objects.all()

@api.post("/languages", response=LanguageSchema, auth=django_auth)
def create_language(request, payload: LanguageCreateSchema):
    language = Language.objects.create(**payload.dict())
    return language

@api.delete("/languages/{language_id}", auth=django_auth)
def delete_language(request, language_id: int):
    language = get_object_or_404(Language, id=language_id)
    language.delete()
    return {"success": True}

# Book Endpoints
@api.get("/books", response=List[BookSchema])
def list_books(request):
    return Book.objects.all()

@api.post("/books", response=BookSchema, auth=django_auth)
def create_book(request, payload: BookCreateSchema):
    book = Book.objects.create(
        title=payload.title,
        author_id=payload.author_id,
        summary=payload.summary,
        isbn=payload.isbn,
        language_id=payload.language_id,
    )
    book.genre.set(payload.genre_ids)
    return book

@api.put("/books/{book_id}", response=BookSchema, auth=django_auth)
def update_book(request, book_id: int, payload: BookCreateSchema):
    book = get_object_or_404(Book, id=book_id)
    for attr, value in payload.dict().items():
        if attr == "genre_ids":
            book.genre.set(value)
        else:
            setattr(book, attr, value)
    book.save()
    return book

@api.delete("/books/{book_id}", auth=django_auth)
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"success": True}

# BookInstance Endpoints
@api.get("/bookinstances", response=List[BookInstanceSchema])
def list_bookinstances(request):
    return BookInstance.objects.all()

@api.post("/bookinstances", response=BookInstanceSchema, auth=django_auth)
def create_bookinstance(request, payload: BookInstanceCreateSchema):
    bookinstance = BookInstance.objects.create(**payload.dict())
    return bookinstance

@api.put("/bookinstances/{bookinstance_id}", response=BookInstanceSchema, auth=django_auth)
def update_bookinstance(request, bookinstance_id: int, payload: BookInstanceCreateSchema):
    bookinstance = get_object_or_404(BookInstance, id=bookinstance_id)
    for attr, value in payload.dict().items():
        setattr(bookinstance, attr, value)
    bookinstance.save()
    return bookinstance

@api.delete("/bookinstances/{bookinstance_id}", auth=django_auth)
def delete_bookinstance(request, bookinstance_id: int):
    bookinstance = get_object_or_404(BookInstance, id=bookinstance_id)
    bookinstance.delete()
    return {"success": True}