from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,  PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault('is_staff', False)  # Add this to ensure superuser gets admin access
        extra_fields.setdefault('is_superuser', False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # Add this to ensure superuser gets admin access
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, unique=True)  # Required
    name = models.CharField(max_length=50)  # Now optional
    age = models.IntegerField(null=True, blank=True)  # Now optional
    national_id_card_no = models.CharField(max_length=20, null=True, blank=True)  # Now optional
    is_active = models.BooleanField(default=False)  # Has default, no need for null/blank
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)  # Auto-set, no need for null/blank
    objects = CustomUserManager()

  
    USERNAME_FIELD = 'email'  # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = ['name'] 

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Custom related_name for groups
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Custom related_name for permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    

class Model(models.Model):
    pass
    name = models.CharField(max_length=100)

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('name',)



class Car(models.Model):
    id = models.AutoField(primary_key=True) 
    model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=100, default='unknown')
    category = models.CharField(max_length=50)
    condition = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    fueltype = models.CharField(max_length=50)
    mileage = models.CharField(max_length=50)
    enginesize = models.CharField(max_length=50)
    cylinder = models.CharField(max_length=50)
    door = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='CarPictures/', null=True, blank=True)

class Sales(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    car = models.ForeignKey(Car, on_delete=models.CASCADE) 
    invoicenumber = models.IntegerField()


class Save(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  
    

class Offers(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
     car = models.ForeignKey(Car, on_delete=models.CASCADE)     

