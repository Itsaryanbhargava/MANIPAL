from django.shortcuts import render, redirect
from .forms import AuthorForm, PublisherForm, BookForm
from .models import Author, Publisher, Book

# Create your views here.

def book_list(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    publishers = Publisher.objects.all()
    return render(request,'book_list.html', {'books': books, 'authors': authors, 'publishers': publishers})

def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})
    
def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = PublisherForm()
    return render(request, 'add_publisher.html', {'form': form})
    
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})
    


