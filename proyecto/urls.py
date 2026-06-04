from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:product_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('pedido/confirmar/', views.confirmar_pedido, name='confirmar_pedido'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('stock/', views.stock, name='stock'),
    path('vender/', views.venta, name='vender'),
    path('mis-productos/', views.productos_vendedor, name='mis_productos'),
    path('tiendas/', views.tiendas, name='tiendas'),
    path('cartas/', views.cartas, name='cartas'),
    path('colecciones/', views.colecciones, name='colecciones'),
    path('contacto/', views.contacto, name='contacto'),
]
# ojo con el id (no exonerlo )

