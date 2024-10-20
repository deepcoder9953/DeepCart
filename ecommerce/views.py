from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Products, Cart, RegisterUser, ShowProduct
from .forms import Producatform, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate



# Create your views here.

def product(request):
    if request.method == 'POST':
        form = Producatform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'product added successsfullly')
            return redirect('product')
        else:
            form = Producatform()
        
    return render(request, 'product.html')

def show(request, name=None):
    if name:
        request.session['name'] = name

    name = request.session.get('name')

    if name:
        products = Products.objects.filter(name=name)
    else:
        products = Products.objects.all()
    if products.exists():
        return render(request, 'show.html', {'products': products})
    else:
        return render(request, 'show.html', {'error': 'No products found'}) 
    
def add_to_cart(request, product_id):
    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        messages.error(request, 'Product not found.')
        return redirect('product_list') 

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1 

    request.session['cart'] = cart
    
    messages.success(request, f'{product.name} has been added to your cart.')
    
    return redirect('show') 

def view_cart(request):
    cart = request.session.get('cart', {})  
    
    if not cart:
        return render(request, 'cart.html', {'message': 'Your cart is empty.'})

    product_ids = cart.keys()  
    products_in_cart = Products.objects.filter(id__in=product_ids) 

    cart_items = []
    for product in products_in_cart:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],
            'price': product.price,
            'img': product.img 
        })

    context = {
        'cart_items': cart_items,
        'cart_total': sum(item['product'].price * item['quantity'] for item in cart_items),
        'img': product.img
        
    }

    return render(request, 'cart.html', context)


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart 
    return redirect('view_cart')

def update_cart(request):
    cart = request.session.get('cart', {})
    
    if request.method == 'POST':
        for product_id, quantity in request.POST.items():
            if product_id != 'csrfmiddlewaretoken':
                cart[product_id] = int(quantity)  
    
        request.session['cart'] = cart  

    return redirect('view_cart') 

def base(request):
    return render(request, 'base.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
            current_site = get_current_site(request)
            activation_link = f'http://{current_site.domain}/activate/{uid}/{token}/'

            subject = 'Activate your account'
            message = render_to_string('activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            send_mail(subject, message, 'sharmadeepanshu576@gmail.com', [user.email])

            return redirect('register_success')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def register_success(request):
    return render(request, 'register_success.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email, password=password)
            if not user.is_active:
                error = "Account not activated. Please check your email."
                return render(request, 'login.html', {'error': error})

            elif user.check_password(password):
                request.session['email'] = email
                request.session['password'] = password
                messages.success(request, "You have been successfully logged in.")
                return redirect('/success',{'error': error})
            else:
                messages.error(request, "There was an error during login.")
                error = "Invalid credentials"
        except User.DoesNotExist:
            error = "Invalid credentials"

        print("successful")
        return redirect('/show',{'error': error})
    
    return render(request, 'login.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(id=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True  
            user.save()
            messages.success(request, "Your account has been activated. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid.")
            return redirect('login')
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        messages.error(request, "Activation link is invalid.")
        return redirect('login')

def search(request):
    query = request.GET.get('query') 
    print(f'Search Query: {query}')
    if query:
        products = Products.objects.filter(name__icontains=query)
    else:
        cart_items = ShowProduct.objects.all()
    
    return render(request, 'search.html', {'cart_items': products, 'query': query})