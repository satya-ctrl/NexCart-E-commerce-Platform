from django.test import TestCase, Client
from django.urls import reverse
from store.models import Product, Category
import json


class AIFeaturesTests(TestCase):
    def setUp(self):
        # Create categories
        self.clothing_cat = Category.objects.create(name="Clothing", slug="clothing")
        self.footwear_cat = Category.objects.create(name="Footwear", slug="footwear")
        
        # Create products
        self.dress = Product.objects.create(
            name="Summer Floral Dress",
            description="Beautiful light summer floral dress with perfect style.",
            category=self.clothing_cat,
            our_price=1500.00,
            amazon_price=1800.00,
            flipkart_price=1750.00,
            rating=4.5,
            brand="Zara",
            tags="dress clothing floral summer",
            reviews_count=20,
            ai_summary="Highly praised for its beautiful print and soft touch."
        )
        
        self.shoes = Product.objects.create(
            name="Running Sneakers",
            description="Next-gen running shoes for sports.",
            category=self.footwear_cat,
            our_price=4500.00,
            amazon_price=4800.00,
            rating=4.8,
            brand="Adidas",
            tags="shoes footwear running sneakers sports",
            reviews_count=45,
            ai_summary="Excellent springy feedback and durable build."
        )
        
        self.client = Client()

    def test_chatbot_greeting_fallback(self):
        response = self.client.post(
            reverse('ai_features:chatbot'),
            data=json.dumps({"message": "Hello shopbot!"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("reply", data)
        self.assertIn("ShopBot AI", data["reply"])
        self.assertIn("Fashion Stylist", data["reply"])

    def test_chatbot_recommendation_fallback(self):
        response = self.client.post(
            reverse('ai_features:chatbot'),
            data=json.dumps({"message": "I need some running shoes"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Running Sneakers", data["reply"])

    def test_chatbot_price_comparison_fallback(self):
        response = self.client.post(
            reverse('ai_features:chatbot'),
            data=json.dumps({"message": "compare price for summer dress"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Summer Floral Dress", data["reply"])
        self.assertIn("Amazon", data["reply"])

    def test_chatbot_sentiment_fallback(self):
        response = self.client.post(
            reverse('ai_features:chatbot'),
            data=json.dumps({"message": "what is review sentiment for running sneakers"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Running Sneakers", data["reply"])
        self.assertIn("Customer Review Sentiment", data["reply"])

    def test_get_recommendation_fallback(self):
        response = self.client.post(
            reverse('ai_features:ai_recommend'),
            data=json.dumps({
                "budget": "2000",
                "category": "Clothing",
                "preferences": "floral dress"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("recommendations", data)
        recs = data["recommendations"]
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["name"], "Summer Floral Dress")
        self.assertGreaterEqual(recs[0]["match_score"], 75)

    def test_analyze_sentiment_fallback(self):
        reviews = [
            "This dress is amazing! The fabric is so soft and fits perfectly.",
            "Really good quality summer floral design.",
            "It is nice but a little loose."
        ]
        response = self.client.post(
            reverse('ai_features:ai_sentiment'),
            data=json.dumps({"reviews": reviews}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["overall_sentiment"], "positive")
        self.assertGreaterEqual(data["score"], 70)
        self.assertIn("positives", data)
        self.assertTrue(len(data["positives"]) > 0)

    def test_smart_search_fallback(self):
        response = self.client.post(
            reverse('ai_features:smart_search'),
            data=json.dumps({"query": "floral dress under 2000"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        results = data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Summer Floral Dress")

    def test_price_prediction_fallback(self):
        response = self.client.post(
            reverse('ai_features:price_predict'),
            data=json.dumps({"product_id": self.dress.id}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("trend", data)
        self.assertIn("predicted_price", data)
        self.assertIn("advice", data)
