from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUser(AbstractUser):
    first_name = models.CharField(
        _('First Name'),
        max_length=20,
        help_text=_(
            'Required. Maximum 20 characters.'
        )
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=20,
        help_text=_(
            'Required. Maximum 20 characters.'
        )
    )
    username = models.CharField(
        _('Username'),
        max_length=20,
        unique=True,
        help_text=_(
            'Required. 4 to 20 characters.Beginning with an alphabet. Letters, digits and @/./+/-/_ only.'
        ),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z][\w@+-.]{3,19}\Z',
                message='Invalid username. Must be 4 to 20 characters long, starting with an alphabet.\
                     Letters, digits and @/./+/-/_ only.'
            )
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('Email'),
        unique=True)

    @property
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['id']
