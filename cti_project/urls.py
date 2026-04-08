from django.contrib import admin
from django.urls import path , include
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from deliberation.views import custom_logout

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('notes/', include('evaluations.urls')),
    path('deliberation/', include('deliberation.urls')),
    path('', include('accounts.urls')),
    path('', include('courses.urls')),
    path('', include('academics.urls')),
    path('', include('payments.urls')),
    path('', include('evaluations.urls')),
    path('payments/', include('payments.urls')),
    path('logout/', custom_logout, name='logout'),
]