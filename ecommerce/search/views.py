
# Search
def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'shop/search.html', {'products': products, 'query': query})
