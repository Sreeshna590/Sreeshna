from shop.models import Category

def link(request):
    c = Category.objects.all()
    return {'link': c}
