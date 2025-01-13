from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Avg
from .models import Product, Review
from .forms import ReviewForm
from progress_store import models

# Create your views here.
def home(request):
    products = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'home.html', {'products':products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()  # Use the related_name from the ForeignKey
    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})

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