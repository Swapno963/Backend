from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class AccountManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone Number field must be set')

        user = self.model(

            phone=phone,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superadmin', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superadmin') is not True:
            raise ValueError(('is_superadmin must have is_superadmin=True.'))
        return self.create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractBaseUser):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=50, null=True, blank=True)

    joined_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_agreed = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'phone', 'email']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='users/profiles/', null=True, blank=True)
	delivery_address = models.CharField(max_length=255)
