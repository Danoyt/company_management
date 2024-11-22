from rest_framework import serializers
from .models import Department, Position, Employee, Permission
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):  # для регистрации пользователя-сотрудника
    class Meta:  # заполняем данные человека
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data): # создаем пользователя, который может стать сотрудником
        user = User.objects.create_user(**validated_data)
        return user

class DepartmentSerializer(serializers.ModelSerializer): # для подразделений
    class Meta:
        model = Department
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer): # для добавления прав для определенной должности
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']

class PositionSerializer(serializers.ModelSerializer): # для должностей
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all()) # указание департамента к которому относится позиция
    permissions = PermissionSerializer(many=True, read_only=True) # для отображения разрешений, связанных с позицией
    permission_ids = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True, write_only=True)

    class Meta:
        model = Position
        fields = ['id', 'name', 'department', 'permissions', 'permission_ids']

    def create(self, validated_data): # создание новой позиции
        permission_ids = validated_data.pop('permission_ids', [])
        position = Position.objects.create(**validated_data)
        position.permissions.set(permission_ids)
        return position

    def update(self, instance, validated_data): # обновление существующей позиции
        permission_ids = validated_data.pop('permission_ids', None)
        if permission_ids is not None:
            instance.permissions.set(permission_ids)
        return super().update(instance, validated_data)

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer() # сериализация данных пользователя, связанного с сотрудником
    positions = PositionSerializer(many=True, read_only=True) # отображение позиций сотрудника
    position_ids = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all(), many=True, write_only=True) # для указания id позиций при создании/обновлении сотрудника

    class Meta:
        model = Employee
        fields = ['id', 'user', 'positions', 'position_ids']

    def create(self, validated_data):  # создание нового сотрудника
        user_data = validated_data.pop('user') # извлекаем данные пользователя
        user = UserSerializer().create(user_data)
        employee = Employee.objects.create(user=user) # делаем пользователя сотрудником
        position_ids = validated_data.pop('position_ids', []) # получаем выбранные позиции, или пустой список если они не выбраны
        employee.positions.set(position_ids)  # назначаем сотруднику выбранные позиции
        return employee

    def update(self, instance, validated_data):  # обновление сотрудника
        position_ids = validated_data.pop('position_ids', None)
        if position_ids is not None:
            instance.positions.set(position_ids)
        return super().update(instance, validated_data)