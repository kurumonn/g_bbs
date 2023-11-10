from django.urls import path
from . import views




app_name    = "g_bbs"
urlpatterns = [
    path('', views.index, name="index"),
    path('refresh/', views.refreshg, name="refreshg"),
    #path('photo/', views.photo, name="photo"),
    #path('document/', views.document, name="document"),
    path('<int:pk>/', views.single, name="single"),
    



]


