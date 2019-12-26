from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Product
def home(request):
    products = Product.objects
    return render(request, 'products/home.html',{'products':products})

@login_required
def create(request):
    if request.method=='POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product=Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            urlch = request.POST['url']
            if urlch.startswith('http://') or urlch.startswith('https://'):
                product.url=urlch
            else:
                product.url='http://'+urlch
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            # product.votes_total = 1             
            product.hunter= request.user
            product.save()
            return redirect('/products/'+str(product.id))
        else:
            return render(request, 'products/create.html',{'error':'Fill all the values'})    


    else:    
        return render(request, 'products/create.html')    
# Create your views here.
def detail(request, product_id):
    product= get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html',{'product':product})
@login_required
def upvote(request,product_id):
    product= get_object_or_404(Product, pk=product_id)
    product.votes_total+=1
    product.save()
    return redirect('/products/'+ str(product.id))
