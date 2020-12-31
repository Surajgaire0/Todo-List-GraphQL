from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

# Create your models here.


class Todo(models.Model):

    class ActiveManager(models.Manager):
        def get_queryset(self):
            return super(ActiveManager, self).get_queryset().filter(is_completed=False)

    class CompletedManager(models.Manager):
        def get_queryset(self):
            return super(CompletedManager, self).get_queryset().filter(is_completed=True)

    title = models.CharField(_('title'), max_length=255)
    detail = models.TextField(_('detail'), blank=True, null=True)
    owner = models.ForeignKey(
        to=get_user_model(), on_delete=models.CASCADE, verbose_name=_('owner'))
    is_important = models.BooleanField(_('is_important'), default=False)
    is_completed = models.BooleanField(_('is_completed'), default=False)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    completed_at = models.DateTimeField(
        _('completed_at'), blank=True, null=True)
    objects = models.Manager()  # default manager
    active = ActiveManager()  # custom manager
    completed = CompletedManager()  # custom manager

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('todo')
        verbose_name_plural = _('todos')
        ordering = ['id']
