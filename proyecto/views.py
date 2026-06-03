from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from .models import User, Product, Category, Cart, CartItem, Order, OrderItem, StockMovement

def stock(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    productos = Product.objects.filter(is_active=True)
    movimientos = StockMovement.objects.all().order_by('-created_at')[:10]
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        movement_type = request.POST.get('movement_type')
        quantity = int(request.POST.get('quantity'))
        reason = request.POST.get('reason')
        
        product = Product.objects.get(id=product_id)
        
        if movement_type == 'in':
            product.stock += quantity
        elif movement_type == 'out':
            if product.stock < quantity:
                messages.error(request, 'Stock insuficiente.')
                return redirect('stock')
            product.stock -= quantity
        
        product.save(update_fields=['stock'])
        
        StockMovement.objects.create(
            tenant=product.tenant,
            product=product,
            movement_type=movement_type,
            quantity=quantity,
            reason=reason,
        )
        
        messages.success(request, 'Movimiento registrado correctamente.')
        return redirect('stock')
    
    return render(request, 'stock.html', {
        'productos': productos,
        'movimientos': movimientos,
    })
    
    
def confirmar_pedido(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        cart = Cart.objects.get(user=request.user, status='active')
    except Cart.DoesNotExist:
        return redirect('carrito')
    
    items = cart.items.select_related('product').all()
    
    if not items:
        return redirect('carrito')
    
    with transaction.atomic():
        order = Order.objects.create(
            tenant=cart.tenant,
            user=request.user,
            status='pending',
            total=0,
        )
        
        total = 0
        for item in items:
            product = item.product
            if product.stock < item.quantity:
                messages.error(request, f'Stock insuficiente para {product.name}.')
                return redirect('carrito')
            
            subtotal = item.unit_price * item.quantity
            total += subtotal
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=subtotal,
            )
            
            product.stock -= item.quantity
            product.save(update_fields=['stock'])
        
        order.total = total
        order.save(update_fields=['total'])
        
        cart.status = 'converted'
        cart.save(update_fields=['status'])
    
    return redirect('mis_pedidos')

def mis_pedidos(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'mis_pedidos.html', {'orders': orders})


def agregar_carrito(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(
        user=request.user,
        tenant=product.tenant,
        status='active'
    )
    
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'unit_price': product.price, 'quantity': 1}
    )
    
    if not created:
        item.quantity += 1
        item.save()
    
    return redirect('carrito')

def carrito(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        cart = Cart.objects.get(user=request.user, status='active')
        items = cart.items.select_related('product').all()
        total = sum(item.unit_price * item.quantity for item in items)
    except Cart.DoesNotExist:
        items = []
        total = 0
    
    return render(request, 'carrito.html', {'items': items, 'total': total})

def eliminar_carrito(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect('carrito')

def catalogo(request):
    categoria_id = request.GET.get('categoria')
    categorias = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    
    if categoria_id:
        products = products.filter(category_id=categoria_id)
    
    return render(request, 'catalogo.html', {
        'products': products,
        'categorias': categorias,
        'categoria_activa': categoria_id,
    })
    
def home(request):
    products = Product.objects.filter(is_active=True)[:6]
    return render(request, 'home.html', {'products': products})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        
        if password != confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe una cuenta con ese correo.')
            return render(request, 'registro.html')
        
        user = User.objects.create_user(username=email, email=email, password=password)
        login(request, user)
        return redirect('home')
    
    return render(request, 'registro.html')

