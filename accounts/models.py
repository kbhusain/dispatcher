# from email.policy import default
# from django.db import models
# import datetime 

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager,
)
from django.db import models
from django.utils import timezone



# pbkdf2_sha256$320000$aA16YpmF1rEVo7DKB8ztrP$FDS2dIEIW38UjyuqtYvNoD/a995Z3i2xHPIUoc1Xe5k=

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """PermissionsMixin contains the following fields:
        - `is_superuser`
        - `groups`
        - `user_permissions`
     You can omit this mix-in if you don't want to use permissions or
     if you want to implement your own permissions logic.
     """

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = 'auth_user'
        # `db_table` is only needed if you move from the existing default
        # User model to a custom one. This enables to keep the existing data.

    USERNAME_FIELD = 'email'
    """Use the email as unique username."""

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    ]

    email = models.EmailField(
        verbose_name=str("email address"), unique=True,
        error_messages={
            'unique':     "A user is already registered with this email address",
        },
    )
    gender = models.CharField(
        max_length=1, blank=True, choices=GENDER_CHOICES,
        verbose_name="gender",
    )
    first_name = models.CharField(
        max_length=30, verbose_name="first name",default="first_name",
    )
    last_name = models.CharField(
        max_length=30, verbose_name= "last name",default="last_name",
    )
    phone_number = models.CharField(
        max_length=30, verbose_name= "phone number",default="+12145551212",
    )


    is_requester = models.BooleanField(
        verbose_name=str("requester"),
        default=False,
        help_text=str(
            "I want to make requests on this site."
        ),
    )
    
    is_producer = models.BooleanField(
        verbose_name=str("producer"),
        default=False,
        help_text=str(
            "I want to volunteer via this site."
        ),
    )
    
    is_staff = models.BooleanField(
        verbose_name=str("staff status"),
        default=False,
        help_text=str(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        verbose_name=str("active"),
        default=True,
        help_text=str(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(
        verbose_name=str("date joined"), default=timezone.now,
    )

    

    objects = UserManager()





# # Create your models here.

# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# class UserManager(BaseUserManager):
#     def create_user(self,email,password=None):
#         if not email:
#             raise ValueError('User must have an email address')
#         user = self.model(email=self.normalize_email(email))        
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_staffuser(self,email,password):
#         if not email:
#             raise ValueError('User must have an email address')
#         user = self.model(email=self.normalize_email(email), 
#         )
#         user.set_password(password)
#         user.staff = True
#         user.save(using=self._db)
#         return user


#     def create_superuser(self,email,password):
#         if not email:
#             raise ValueError('User must have an email address')
#         user = self.model(email=self.normalize_email(email), 
#         )
#         user.set_password(password)
#         user.staff = True
#         user.admin = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name='email address', max_length=255, unique=True
#     )
#     is_active = models.BooleanField(default=True)
#     staff = models.BooleanField(default=True)
#     admin = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(default=datetime.datetime.now)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['email']

#     def get_full_name(self):
#         return self.email
    
#     def get_short_name(self):
#         return self.email_field

#     def __str__(self): 
#         return self.email


#     def has_perm(self,perm,obj=None):
#         return True;

#     def has_module_perms(self,app_label):
#         return True; self

#     @property
#     def is_staff(self):
#         return self.staff

#     @property
#     def is_admin(self):
#         return self.admin

#     objects = UserManager()
