from django.forms import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg
from django.urls import reverse
from .models import Product, Review, Category
from .forms import ReviewForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .forms import CustomerRegistrationForm
from django.db.models import Q

# Create your views here.
def home(request):
    products = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'home.html', {'products': products})

def category(request, cat_name):
    cat_name = cat_name.replace('-', ' ')
    try:
        category = Category.objects.get(name__iexact=cat_name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.error(request, 'The category is empty or does not exist')
        return redirect('home')

def login_user(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                raise ValidationError("Username and password are required.")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if email is verified
                if not user.customerprofile.email_verified:
                    messages.error(request, "Email not verified. Please check your inbox.")
                    return render(request, 'login.html', {'error': 'Email not verified.'})
                
                login(request, user)
                return redirect('/admin/') if user.is_staff else redirect('/')
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})

        return render(request, 'login.html')

    except ValidationError as ve:
        return render(request, 'login.html', {'error': str(ve)})
    except Exception:
        return render(request, 'login.html', {'error': 'An unexpected error occurred. Please try again.'})

def logout_user(request):
    logout(request)
    messages.success(request, ("Thanks for Shopping with us..."))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            return _extracted_from_register_user_5(form, request)
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register.html', {'form': form})  


# TODO Rename this here and in `register_user`
def _extracted_from_register_user_5(form, request):
    user = form.save(commit=False)
    user.is_active = False  # deactivate until email is confirmed
    user.save()
    form.save_m2m()

    # Email verification
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = request.build_absolute_uri(
        f"/verify-email/{uid}/{token}/"
    )

    message = render_to_string('verify_email.html', {
        'user': user,
        'verification_link': verification_link
    })

    send_mail(
        subject='Verify Your Email - Progress Store',
        message='This is an HTML email',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=message
    )

    messages.success(request, "Check your email to verify your account.")
    return redirect('login') 

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        user.customerprofile.email_verified = True
        user.customerprofile.save()
        messages.success(request, "Email verified! You can now log in.")
    else:
        messages.error(request, "Invalid or expired verification link.")

    return redirect('login') 

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
            return _extracted_from_submit_review_6(form, product, request)
    else:
        form = ReviewForm()
    return render(request, 'submit_review.html', {'form': form, 'product': product})


# TODO Rename this here and in `submit_review`
def _extracted_from_submit_review_6(form, product, request):
    review = form.save(commit=False)
    review.product = product
    review.customer = request.user.customer  # Assuming logged-in users are linked to customers
    review.save()
    # Update product's average rating
    product.average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
    product.save()
    return redirect('product_detail', product_id=product.id)
