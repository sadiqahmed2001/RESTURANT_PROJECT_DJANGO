"""
URL configuration for foodproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from foodapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index,name='index'),
    path('base/',views.base),
    path('register/',views.register,name='register'),
    path('ulogin/',views.ulogin,name='login'),
    path('ulogout/',views.ulogout,name='ulogout'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/otp/', views.password_reset_otp, name='password_reset_otp'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('head/',views.head),
    path('headlink/',views.headlink),
    path('footer/',views.footer),
    path('menu/',views.menu),
    path('filterbycategory/<cid>/',views.filterbycategory,name="filterbycategory"),
    path('filterbytype/<tid>/',views.filterbytype,name="filterbytype"),
    path('addtocart/<mid>/',views.addtocart,name="addtocart"),
    path('viewcart/',views.viewcart,name="viewcart"),
    path('removecart/<cid>/',views.removecart),
    path('updateqty/<x>/<cid>/',views.updateqty),
    path('conformorder/',views.conformorder),
    path('track/',views.track),
    path('fetchorder/',views.fetchorder),
    path('makepayment/',views.makepayment,name="makepayment"),
    path('paymentsuccess/',views.paymentsuccess,name="paymentsuccess"),
    # path('payment_weebhook/',views.payment_webhook),
    path('about/',views.about),
    path('contact/',views.contact,name="contact"),
    path('queryviews/',views.queryviews),
    path('savebooking/',views.savebooking,name="savebooking"),
    path('reservation_view/',views.reservation_view),
    path('testimonial/',views.testimonial,name="testimonial"),
    path('reviews/',views.reviews,name="reviews"),
    path('service/',views.service),
    path('post_list/',views.post_list),
    path('team/', views.team, name='team'),
    
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
