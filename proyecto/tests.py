from django.test import TestCase, Client
from django.urls import reverse
from .models import Tenant, User, Category, Product

class TenantModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name='Tienda Test',
            slug='tienda-test',
            is_active=True
        )

    def test_tenant_creado(self):
        self.assertEqual(self.tenant.name, 'Tienda Test')
        self.assertTrue(self.tenant.is_active)

    def test_tenant_str(self):
        self.assertEqual(str(self.tenant), 'Tienda Test')


class UserModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name='Tienda Test',
            slug='tienda-test2',
        )
        self.user = User.objects.create_user(
            username='test@test.com',
            email='test@test.com',
            password='test1234',
            tenant=self.tenant,
            role='customer'
        )

    def test_user_creado(self):
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.role, 'customer')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'test@test.com')


class ProductModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name='Tienda Test',
            slug='tienda-test3',
        )
        self.category = Category.objects.create(
            tenant=self.tenant,
            name='Cartas',
            slug='cartas'
        )
        self.product = Product.objects.create(
            tenant=self.tenant,
            category=self.category,
            name='Pikachu Test',
            price=100.00,
            stock=10,
            is_active=True
        )

    def test_product_creado(self):
        self.assertEqual(self.product.name, 'Pikachu Test')
        self.assertEqual(self.product.stock, 10)

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Pikachu Test')

    def test_product_activo(self):
        self.assertTrue(self.product.is_active)


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tenant = Tenant.objects.create(
            name='Tienda Test',
            slug='tienda-test4',
        )
        self.user = User.objects.create_user(
            username='test@test.com',
            email='test@test.com',
            password='test1234',
            tenant=self.tenant,
        )

    def test_home_carga(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_carga(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_catalogo_carga(self):
        response = self.client.get(reverse('catalogo'))
        self.assertEqual(response.status_code, 200)

    def test_login_correcto(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@test.com',
            'password': 'test1234'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_incorrecto(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@test.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_carrito_sin_login_redirige(self):
        response = self.client.get(reverse('carrito'))
        self.assertEqual(response.status_code, 302)

    def test_registro_carga(self):
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)