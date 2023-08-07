from django.urls import path
from . import views

#router=routers.SimpleRouter()

urlpatterns = [

    path('', views.homepage, name='homepage'),

]			