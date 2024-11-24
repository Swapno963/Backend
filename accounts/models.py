from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class AccountManager(BaseUserManager):

	def create_user(self, phone, password=None, **extra_fields):
		if not phone:
			raise ValueError('phone number field must be set')

		user = self.model(
	        phone=phone,
	        **extra_fields
	    )
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('role', 'super_admin')
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superadmin', True)
		extra_fields.setdefault('is_admin', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superadmin') is not True:
			raise ValueError('Superuser must have is_superadmin=True.')
		
		return self.create_user(email=email, password=password, **extra_fields)



class CustomUser(AbstractBaseUser):

	ROLE_CHOICES = [
        ('super_admin', 'super_admin'),
        ('supplier', 'supplier'),
        ('customer', 'customer'),
    ]
	
	name = models.CharField(max_length=30)
	phone = models.CharField(max_length=15, unique=True)
	email = models.EmailField(max_length=50, null=True, blank=True)
	role = models.CharField(choices=ROLE_CHOICES, max_length=30, default='customer')

	joined_date = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_agreed = models.BooleanField(default=True)
	is_superadmin = models.BooleanField(default=False)

	USERNAME_FIELD = 'phone'
	REQUIRED_FIELDS = ['name', 'email']

	objects = AccountManager()

	def __str__(self):
		return self.phone

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, add_label):
		return True

	def is_super_admin(self):
		return self.role == 'super_admin'

	def is_supplier(self):
		return self.role == 'supplier'

	def is_customer(self):
		return self.role == 'customer'

	def save(self, *args, **kwargs):

		super().save(*args, **kwargs)

		if self.is_supplier:
			supp_exist = SupplierProfile.objects.filter(user=self).exists()
			if not supp_exist:
				SupplierProfile.objects.create(user=self)
		if self.is_customer:
			user_exist = UserProfile.objects.filter(user=self).exists()
			if not user_exist:
				UserProfile.objects.create(user=self)



class UserProfile(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='users/profiles/', null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	street_address = models.CharField(max_length=255, null=True, blank=True)


	


class SupplierProfile(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='supplier/profile/', null=True, blank=True)
	address = models.CharField(max_length=300, null=True, blank=True)
	street_address = models.CharField(max_length=255, null=True, blank=True)
	license = models.ImageField(upload_to='supplier/license/', null=True, blank=True)
	documents = models.ImageField(upload_to='supplier/documents/', null=True, blank=True)

