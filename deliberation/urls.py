from django.urls import path
from . import views 
from . import views_admin
from .views import custom_logout
from .views import admin_deliberation_view, student_login, student_dashboard, export_excel_view, student_pdf_view
urlpatterns = [
    path('login/', views.student_login, name='student_login'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('result/', views.student_result, name='student_result'),
    path('admin/dashboard/', views_admin.admin_dashboard, name='admin_dashboard'),
    path('admin/students/', views_admin.admin_students, name='admin_students'),
    path('admin/student/<int:student_id>/', views_admin.admin_student_detail, name='admin_student_detail'),
    path('deliberation/<int:promotion_id>/', admin_deliberation_view, name='admin_deliberation'),
    path('login/', student_login, name='student_login'),
    path('dashboard/', student_dashboard, name='student_dashboard'),
    path('logout/', custom_logout, name='logout'),
    path('export-excel/<int:promotion_id>/', export_excel_view, name='export_excel'),
    path('bulletin/<int:student_id>/', student_pdf_view, name='student_pdf'),

]