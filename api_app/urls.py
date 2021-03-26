from django.urls import path
from api_app import views

app_name = 'api'

urlpatterns = [
    path('', views.api_root, name='root'),
    path('details/', views.DetailList.as_view(), name='detail-list'),
    path('details/<int:pk>/', views.DetailDetail.as_view(), name='detail-detail'),
    path('reports/', views.ReportList.as_view(), name='report-list'),
    path('reports/<int:pk>/', views.ReportDetail.as_view(), name='report-detail'),
    path('report-lines/', views.ReportLineList.as_view(), name='report-line-list'),
    path('report-lines/<int:pk>/', views.ReportLineDetail.as_view(), name='report-line-detail'),
]