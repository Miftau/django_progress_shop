from django.forms import ValidationError
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
    try:
        if request.method == 'POST':
            print(f"Request method: {request.method}")
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(f"Username: {username}, Password: {password}")

            if not username or not password:
                raise ValidationError("Username and password are required.")

            user = authenticate(request, username=username, password=password)
            print(f"Authenticated user: {user}")
            if user is not None:
                login(request, user)
                # Redirect to the admin dashboard if the user is an admin
                if user.is_staff:
                    return redirect('/admin/')
                else:
                    return redirect('/')  # Redirect to the homepage for non-admin users
            else:
                # Handle invalid credentials
                print("Invalid credentials")
                return render(request, 'login.html', {'error': 'Invalid username or password'})

        # For GET requests, render the login page
        print("Rendering login page")
        return render(request, 'login.html')

    except ValidationError as ve:
        # Handle form validation errors
        return render(request, 'login.html', {'error': str(ve)})
    except Exception as e:
        # Catch-all for unexpected exceptions
        return render(request, 'login.html', {'error': 'An unexpected error occurred. Please try again.'})

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