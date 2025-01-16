from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg
from django.urls import reverse
from .models import Product, Review
from .forms import ReviewForm
from progress_store import models
from django.contrib import messages

# Create your views here.
def home(request):
    products = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'home.html', {'products':products})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You are welcome to PROGRESS STORE"))
            return redirect('home')
        else:
            messages.success(request, ("Invalid Login, please check again or retrieve password"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Thanks for Shopping with us..."))
    return redirect('home') 

def about(request):
    home_url = reverse('home')  
    return render(request, 'about.html', {'home_url': home_url})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'form': form,
        'reviews': reviews,
    })

def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.customer = request.user.customer  # Assuming logged-in users are linked to customers
            review.save()
            # Update product's average rating
            product.average_rating = product.reviews.aggregate(models.Avg('rating'))['rating__avg']
            product.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'submit_review.html', {'form': form, 'product': product})