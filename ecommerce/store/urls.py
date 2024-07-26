from django.urls import path

from.import views

urlpatterns = [
	path("login/",views.user_login,name='login'),
	path("signup/",views.signup,name='signup'),
	path("logout", views.logout_, name='logout'),

	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('product/<int:product_id>/', views.view_description_product, name='view_product'),

]