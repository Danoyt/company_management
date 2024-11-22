from django.db import models
from django.contrib.auth.models import User, Permission

class Department(models.Model): # модель для подразделения
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.name

class Position(models.Model): # модель для должности
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions')
    permissions = models.ManyToManyField(Permission, related_name='positions')

    def __str__(self):
        return self.name

class Employee(models.Model): # модель для сотрудника
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    positions = models.ManyToManyField(Position, related_name='employees')

    def __str__(self):
        return self.user.username

