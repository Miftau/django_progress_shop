from django import forms
from .models import Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomerProfile

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Stars') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
        
class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            profile = user.customerprofile
            profile.profile_picture = self.cleaned_data['profile_picture']
            profile.save()
        return user
