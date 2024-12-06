from django.urls import path
from .views import CategoryListCreateAPIView, ProductListCreateAPIView, CardListView, CardCreateView, \
    CommentListCreateView, CommentRetrieveUpdateDestroyView

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('cards/', CardCreateView.as_view(), name='card-create'),
    path('my-cards/', CardListView.as_view(), name='my-cards'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),
]
