from django.db import models
from django.contrib.auth.models import AbstractUser

from customuser.managers import CustomUserManager
from django.utils.translation import gettext as _
from .validators import validate_phone_number
from multiselectfield import MultiSelectField


class NewUser(AbstractUser):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )
    username = None
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    phone = models.CharField(
        _("Phone No."), max_length=10, unique=True, validators=[validate_phone_number]
    )
    dob = models.DateField(_("Date Of Birth"), blank=True, null=True)
    gender = models.CharField(
        _("Gender"), max_length=10, choices=GENDER_CHOICES, default=""
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"  # make the user log in with the email
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserInfo(models.Model):
    """
    User Info model to save user information.
    This is related with user table through OneToOne relation.
    """

    HOBBY_CHOICES = (
        ("sport", ("sport")),
        ("music", ("music")),
        ("travel", ("travel")),
        ("other", ("other")),
    )
    user = models.OneToOneField(
        NewUser,
        related_name="user_info",
        on_delete=models.CASCADE,
    )
    age = models.SmallIntegerField(default=0)
    hobbies = MultiSelectField(
        _("Hobbies"), max_length=50, choices=HOBBY_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.first_name}"
