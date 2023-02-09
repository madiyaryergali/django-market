from django.shortcuts import redirect, render
from item.models import Item, Category
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all( )
    return render(request, 'core/index.html',
    {
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html',{
        'form':form,
    })
