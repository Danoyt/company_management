from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from structure.views import DepartmentViewSet, PositionViewSet, EmployeeViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('structure.urls')),  # Добавьте этот маршрут для корневого URL-адреса
]