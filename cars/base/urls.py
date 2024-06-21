from django.urls import path
from  .import views



urlpatterns = [
    
 
    path('', views.home, name='home') ,
    path('car/<str:pk>/', views.car, name='car') ,
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #path('register/', views.register_page, name='register'),
    path('register/', views.register_page, name='user-form'),
    path('update-user/<str:pk>/', views.update_user, name='update-user'),  
    
    path('', views.available_cars, name='available_cars'),  # Home page 
    path('book/<int:car_id>/', views.book_car, name='book_car'),  
    path('car/<str:pk>/', views.car,  name='car'),
    
    
]