from django.urls import path, include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.contrib.auth import logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index_page, name='index_page'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('schedule_my/', views.schedule_my, name='schedule_my'),
    path('my_tutor/', views.my_tutor, name='my_tutor'),
    path('schedule_tutor/<int:pk>/', views.schedule_tutor, name='schedule_tutor'),
    path('invoice_unpaid/', views.invoice_unpaid, name='invoice_unpaid'),
    path('invoice_paid/', views.invoice_paid, name='invoice_paid'),
    path('notification/', views.notification, name='notification'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('logout/', views.user_logout, name='user_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
