from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Product, Category

# ✅ User Registration Form
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user

# ✅ Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))



# ✅ Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # Includes all fields from the Product model

# ✅ Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'desc', 'image']  # Ensure field names match your model




from django import forms
from shop.models import Product
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Forms
class StockForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'stock']

# Views
@login_required
def add_stock(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.stock += form.cleaned_data['stock']  # Increment stock
            product.save()
            return redirect('shop:product_list')  # Redirect to product list or desired page
    else:
        form = StockForm()
    return render(request, 'shop/addstock.html', {'form': form})
