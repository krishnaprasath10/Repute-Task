from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Book
from django.contrib import messages

# Book list
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

# Add book
@login_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        isbn = request.POST.get('isbn')

        if not title or not author or not published_date or not isbn:
            messages.error(request, "All fields are required.")
        else:
            Book.objects.create(
                title=title,
                author=author,
                published_date=published_date,
                isbn=isbn,
                created_by=request.user
            )
            return redirect('book_list')

    return render(request, 'add_book.html')

# Edit book
@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk, created_by=request.user)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.published_date = request.POST.get('published_date')
        book.isbn = request.POST.get('isbn')
        book.save()
        return redirect('book_list')
    return render(request, 'edit_book.html', {'book': book})

# Delete book
@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk, created_by=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'delete_book.html', {'book': book})

# Signup (manual form)
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('book_list')

    return render(request, 'signup.html')

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('book_list')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'login.html')

# Logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('book_list')
