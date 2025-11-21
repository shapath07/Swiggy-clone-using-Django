from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[ 
    path("", views.home, name="home"),
    path("categories/", views.category_list, name="categories"),
    path("products/", views.product_list, name="products"),
    path("orders/", views.order_list, name="orders"),
    path("profile/", views.profile_view, name="profile"),
    path("signup/",views.signup_view,name='signup'),
    path("login/",views.login_view,name='login'),
    path("logout/",views.logout_view,name='logout'),
    path('category/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('add_to_cart/<int:id>',views.add_to_cart, name = "add_to_cart"),
    path('coupon/',views.apply_coupon,name = "coupon"),
    path('Your_cart/',views.cart,name ='Your_cart'),
    path('cancel/<int:id>/',views.cancelfromcart,name='cancel_cart'),
    path("place_order/", views.place_order, name="place_order"), 
    path("detail/<str:name>",views.view_details,name="details"),
    path("cancel_order/<int:id>", views.cancel_order, name="cancel_order")
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)