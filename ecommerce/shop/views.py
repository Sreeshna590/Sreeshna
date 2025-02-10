from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView,UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Product, Category
from shop.forms import ProductForm, CategoryForm,StockForm

# Home Page (Category List)
class CategoryListView(ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"

# Product List in Category
class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"


# Product Detail View
class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, LoginForm

# ✅ Register View
def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect("shop:category")  # Redirect to homepage
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})

# ✅ Login View
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("shop:category")  # Redirect to homepage
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

# ✅ Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect("shop:category")  # Redirect to login page after logout



class AddProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('shop:product_list')

# ✅ Add Category View
class AddCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'add_category.html'
    success_url = reverse_lazy('shop:category_list')

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
    return render(request, 'addstock.html', {'form': form})


