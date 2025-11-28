from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def all_with_deleted(self):
        return super().get_queryset()

    def only_deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    
    objects = SoftDeleteManager()
    
    class Meta:
        abstract = True
    
    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
    
    def restore(self):
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])
    
    def is_deleted(self):
        return self.deleted_at is not None
