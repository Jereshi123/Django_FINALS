from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """Manager that filters out soft-deleted records by default"""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def all_with_deleted(self):
        """Get all records including deleted ones"""
        return super().get_queryset()

    def only_deleted(self):
        """Get only soft-deleted records"""
        return super().get_queryset().filter(deleted_at__isnull=False)


class SoftDeleteModel(models.Model):
    """Abstract base model that adds soft delete functionality"""
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    
    objects = SoftDeleteManager()
    
    class Meta:
        abstract = True
    
    def soft_delete(self):
        """Soft delete the record"""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
    
    def restore(self):
        """Restore a soft-deleted record"""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])
    
    def is_deleted(self):
        """Check if record is soft-deleted"""
        return self.deleted_at is not None
