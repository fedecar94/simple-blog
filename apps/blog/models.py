from ckeditor.fields import RichTextField
from django.db import models
from django.utils.text import slugify


# Create your models here.


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, db_index=True)
    published = models.BooleanField(default=False, db_index=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, editable=False)
    content = RichTextField(config_name='awesome_ckeditor')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title


class Comment(BaseModel):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, db_index=True)
    published = models.BooleanField(default=False, db_index=True)
    message = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.author} - {self.created}"
