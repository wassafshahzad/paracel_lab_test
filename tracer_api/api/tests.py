from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class ListOrderAPIViewTests(APITestCase):
    fixtures = ["order_model.json"]

    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('orders-list')
        self.detail_url = reverse('orders-detail', kwargs={'tracking_number': "TN12345679"})

    def test_list_orders(self):
        """ Test list URL to verify correct objects are fetched."""

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_list_orders_query_param(self):
        """Test list URL to verify correct objects are fetched using query params."""


        response = self.client.get(self.list_url, {'carrier': 'DHL'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(self.list_url, {'carrier': 'UPSA'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        response = self.client.get(self.list_url, {'carrier': 'DHL', 'tracking_number': "TN12345678"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

