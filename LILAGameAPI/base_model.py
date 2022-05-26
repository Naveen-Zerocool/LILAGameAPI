import uuid as uuid
from django.db import models

from LILAGameAPI.base_manager import GlobalBaseManager


class GlobalBaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GlobalBaseManager()
    all_objects = models.Manager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if update_fields:
            update_fields.append('updated_at')
        super(GlobalBaseModel, self).save(force_insert=force_insert, force_update=force_update,
                                          using=using, update_fields=update_fields)

    class Meta:
        abstract = True
        get_latest_by = "created_at"
        ordering = ["-created_at", ]
