# PokeMarket

Marketplace multitenant para comprar y vender cartas y productos Pokémon.

## Stack

- Python
- Django
- PostgreSQL

## Funcionalidades

- Registro e inicio de sesión
- Catalogo de productos con filtros por categoría
- Carrito de compras
- Confirmar pedidos
- Mis pedidos
- Dashboard con estadísticas
- Panel de administración

## Instalación

1. Clona el repositorio
   git clone https://github.com/ru0505/pokemarket.git

2. Instala las dependencias
   pip install django psycopg2-binary

3. Configura la base de datos en settings.py
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'pokemarket',
           'USER': 'postgres',
           'PASSWORD': 'tu_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }

4. Corre las migraciones
   python manage.py migrate

5. Crea un superusuario
   python manage.py createsuperuser

6. Corre el servidor
   python manage.py runserver

## Estructura

pokemarket/
    pokemarket/
        settings.py
        urls.py
    proyecto/
        models.py
        views.py
        urls.py
        admin.py
    templates/
        home.html
        login.html
        registro.html
        catalogo.html
        carrito.html
        mis_pedidos.html
        dashboard.html
    static/
        css/
            styles.css

## Modelos

- Tenant - Tiendas independientes
- User - Usuarios con rol y tenant
- Category - Categorías de productos
- Product - Productos por tienda
- Cart - Carrito de compras
- CartItem - Items del carrito
- Order - Pedidos
- OrderItem - Items del pedido
- Coupon - Cupones de descuento
- Review - Reseñas de productos
- StockMovement - Movimientos de inventario