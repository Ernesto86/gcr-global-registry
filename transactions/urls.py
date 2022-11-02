from django.urls import path

from transactions.view.shopping_cart import ShoppingCartView, ShoppingCartBuyView

app_name = 'transactions'

urlpatterns = [
    path('shopping-cart', ShoppingCartView.as_view(), name='shopping_cart'),
    path('shopping-cart/buy', ShoppingCartBuyView.as_view(), name='shopping_cart_buy'),
]