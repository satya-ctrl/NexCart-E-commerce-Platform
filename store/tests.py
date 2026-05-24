from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse

class SellerAuthTests(TestCase):
    def setUp(self):
        self.seller_group, _ = Group.objects.get_or_create(name='Sellers')
        self.seller_user = User.objects.create_user(username='seller1', password='Sellerpass123!')
        self.seller_user.groups.add(self.seller_group)
        self.customer_user = User.objects.create_user(username='customer1', password='Customerpass123!')

    def test_dashboard_redirects_unauthenticated(self):
        response = self.client.get(reverse('store:seller_dashboard'))
        # Should redirect to seller login page
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('store:seller_login'), response.url)

    def test_dashboard_redirects_customer_non_seller(self):
        self.client.login(username='customer1', password='Customerpass123!')
        response = self.client.get(reverse('store:seller_dashboard'))
        # Should log customer out and redirect to seller login page
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('store:seller_login'), response.url)
        # Check that session user is logged out (no user in context)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_dashboard_accessible_by_seller(self):
        self.client.login(username='seller1', password='Sellerpass123!')
        response = self.client.get(reverse('store:seller_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/seller.html')

    def test_seller_register_success(self):
        response = self.client.post(reverse('store:seller_register'), {
            'username': 'new_seller',
            'email': 'new_seller@example.com',
            'first_name': 'New',
            'last_name': 'Seller',
            'password1': 'Sellerpass123!',
            'password2': 'Sellerpass123!'
        })
        self.assertEqual(response.status_code, 302) # Redirects to dashboard
        self.assertTrue(User.objects.filter(username='new_seller').exists())
        user = User.objects.get(username='new_seller')
        self.assertTrue(user.groups.filter(name='Sellers').exists())

    def test_seller_login_success(self):
        response = self.client.post(reverse('store:seller_login'), {
            'username': 'seller1',
            'password': 'Sellerpass123!'
        })
        self.assertEqual(response.status_code, 302) # Redirects to dashboard

    def test_seller_login_fail_for_customer(self):
        response = self.client.post(reverse('store:seller_login'), {
            'username': 'customer1',
            'password': 'Customerpass123!'
        })
        # Should redirect back to login or fail because customer1 is not a seller
        self.assertEqual(response.status_code, 302) # redirects to seller login with error
        self.assertNotIn('_auth_user_id', self.client.session)
