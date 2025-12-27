from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100, unique=True,validators=[RegexValidator(regex='^[A-Za-zÀ-ÖØ-öø-ÿ0-9 _-]+$', message='Title can only contain letters, numbers, spaces, hyphens, and underscores.')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.title