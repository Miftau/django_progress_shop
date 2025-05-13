from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category, Customer, Product, Order, Review
from .models import CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_verified']

# Function for duplicating selected objects in the list view
def duplicate_objects(modeladmin, request, queryset):
    for obj in queryset:
        obj.pk = None  # Reset the primary key to create a new instance
        obj.save()
    model_name = queryset.model._meta.verbose_name_plural.title()
    messages.success(request, f"Selected {model_name} were duplicated successfully.")

duplicate_objects.short_description = "Duplicate selected objects"

# Base admin class for duplication functionality
class BaseAdmin(admin.ModelAdmin):
    actions = [duplicate_objects]  # Add duplication action to list view

    # Adding a duplicate button on the detail page
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:object_id>/duplicate/', self.duplicate_view, name=f'duplicate_{self.model._meta.model_name}'),
        ]
        return custom_urls + urls

    def duplicate_view(self, request, object_id):
        """Handle the view for duplicating a single object."""
        original_object = get_object_or_404(self.model, pk=object_id)

        if request.method == "POST":  # Handle form submission
            original_object.pk = None  # Reset primary key to duplicate
            # Customize duplicated fields if necessary
            if hasattr(original_object, 'name'):
                original_object.name = f"{original_object.name} (Copy)"
            original_object.save()

            self.message_user(request, f"'{original_object}' was duplicated successfully.")
            return redirect(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist')

        # Render a confirmation page for duplication
        context = {
            'title': f'Duplicate {self.model._meta.verbose_name}',
            'object': original_object,
            'opts': self.model._meta,
        }
        return render(request, 'admin/duplicate_confirmation.html', context)


# Register models with duplication features
@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ['name', 'description']  # Use fields defined in the Category model

@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    list_display = ['firstname', 'lastname', 'address', 'phone', 'email']  # Fields from the Customer model

@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ['name', 'description', 'price', 'Category', 'average_rating']  # Fields from the Product model
    list_filter = ['Category']  # Optional: Add filtering by category
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating', 'created_at')

@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = ['product', 'customer', 'quantity', 'address', 'phone', 'date', 'status']  # Fields from the Order model
    list_filter = ['date', 'status']  # Optional: Add filtering by date and status

