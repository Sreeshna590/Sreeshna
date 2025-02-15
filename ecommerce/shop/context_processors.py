from .models import Category

def category_links(request):
    links = Category.objects.all()  # Fetch all categories
    return {'links': links}  # This will be available in all templates
