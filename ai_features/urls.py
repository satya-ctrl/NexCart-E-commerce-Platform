from django.urls import path
from . import views

app_name = 'ai_features'

urlpatterns = [
    path('chatbot/', views.chatbot, name='chatbot'),
    path('recommend/', views.get_recommendation, name='ai_recommend'),
    path('sentiment/', views.analyze_sentiment, name='ai_sentiment'),
    path('smart-search/', views.smart_search, name='smart_search'),
    path('price-predict/', views.price_prediction, name='price_predict'),
    path('dashboard/', views.ai_dashboard, name='ai_dashboard'),
]
