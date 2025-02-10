from django.shortcuts import render, redirect
from book.models import Book

def home(request):
    return render(request, 'home.html')

def addbooks(request):
    if request.method == "POST":
        tit = request.POST['t']
        aut = request.POST['a']
        pri = request.POST['p']
        lan = request.POST['l']
        pag = request.POST['pg']
        img = request.FILES['i']
        pdf = request.FILES['d']
        b = Book.objects.create(title=tit, author=aut, price=pri, language=lan, pages=pag, images=img, pdf=pdf)
        b.save()
        return redirect("book:home")  # Ensure 'home' is the correct URL pattern name
    return render(request, 'addbooks.html')

def viewbooks(request):
    b = Book.objects.all()
    context = {'book': b}
    return render(request, 'viewbooks.html', context)

def factorial(request):
    if request.method == "POST":
        num = int(request.POST['f'])
        f = 1
        for i in range(1, num + 1):
            f = f * i
        return render(request, 'factorial.html', {'fact': f})
    return render(request, 'factorial.html')


def detail(request,i):
    b=Book.objects.get(id=i)
    context={'book':b}
    return render(request,'detail.html',context)


def deletebook(request,i):
    b=Book.objects.get(id=i)
    b.delete()
    return redirect('book:viewbooks')

def edit(request,i):
    b=Book.objects.get(id=i)

    if request.method == "POST":
        b.title=request.POST['t']
        b.author = request.POST['a']
        b.price = request.POST['p']
        b.language = request.POST['la']
        b.pages = request.POST['pg']
        if(request.FILES.get(i)==None):
            b.save()
        else:
            b.img= request.FILES.get('i')
        if (request.FILES.get(i) == None):
            b.save()
        else:
            b.pdf = request.FILES.get('d')
        b.save()
    return render(request, 'edit.html')

def searchbooks(request):
    return render(request,'search.html')
