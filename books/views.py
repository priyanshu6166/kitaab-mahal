from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Comment

# Create your views here.

def home(request):
    books = Book.objects.all()
    return render(request, 'books/home.html', {'books': books})

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = book.comments.order_by('-created_at')
    if request.method == 'POST':
        text = request.POST.get('comment')
        if text:
            Comment.objects.create(book=book, user=request.user, text=text)
            return redirect('book_detail', book_id=book.id)
    return render(request, 'books/book_detail.html', {'book': book, 'comments': comments})
