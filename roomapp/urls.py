from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("customerdata/",views.customerdata,name="customerdata"),
    path("get_user/",views.get_user,name="get_user"),

    path('checkin/', views.checkin, name='checkin'),
    path('checkin_edit/<int:pk>/', views.checkin_edit, name='checkin_edit'),
    path('checkout/', views.checkout, name='checkout'),
    path('addroom/', views.addroom, name='addroom'),
    path('reserveroom/', views.reserveroom, name='reserveroom'),
    path('reservation_edit/<int:pk>/', views.reservation_edit, name='reservation_edit'),
    path('reservation_checkin/', views.reservation_checkin, name='reservation_checkin'),
    path('reservation_cancle/', views.reservation_cancle, name='reservation_cancle'),
    path('roommanager/', views.roommanager, name='roommanager'),
    path("room_update/",views.room_update,name="room_update"),
    path("room_delete/<str:pk>/",views.room_delete,name="room_delete"),
    path("report_gen/",views.report_gen,name="report_gen"),

    path('report/', views.customerdetail, name='report'),
    path('signin/', views.user_login, name='signin'),  
    path('signup/', views.user_signup, name='signup'),  
    path('logout/', views.user_logout, name='logout'),  
    path('with_room/', views.with_room, name='withroom'),
    
    path("withroom_update/<int:pk>/",views.order_update,name="withroom_update"),
    path("withroom_delete/<int:pk>/",views.order_delete,name="withroom_delete"),

    path('resturant/with_out_room/', views.with_out_room, name='withoutroom'),
    path('resturant/with_out_room_update/<int:pk>/', views.with_out_room_update, name='withoutroom_update'),
    path('resturant/with_out_room_delete/<int:pk>/', views.with_out_room_delete, name='withoutroom_delete'),
    
    path("get_room_by_group/",views.get_room_by_group,name="get_room_by_group"),
    path("check_out_process/",views.check_out_process,name="check_out_process"),
    path("check_out/",views.check_out,name="check_out"),


   
]