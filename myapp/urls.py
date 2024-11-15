from . import views
from django.contrib import admin
from django.urls import path,include

'''
urlpatterns = [
    path('admin/', admin.site.urls),
    
    #initial is login
    path('',views.login,name='login'),

    path('login',views.login , name='login'),

    #for the ticket booking , we may have many different possible paths
    path('book/<int:train_id>/<str:seat_class>/<int:no_of_seats>/', views.book_ticket, name='book_ticket')
]
'''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('login_user', views.login_user, name='login_user'),
    path('register_user', views.register_user, name='register_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('train_list', views.train_list, name='train_list'),
    path('book_train/<int:train_id>/<str:seat_class>/<int:no_of_seats>', views.book_train, name='book_train'),
    path('validate_credit_card/<int:ticket_id>', views.validate_credit_card, name='validate_credit_card'), 
    path('booking_confirmation/<int:ticket_id>', views.booking_confirmation, name='booking_confirmation')  
]