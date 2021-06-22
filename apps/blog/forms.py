from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Post


class PostAdminForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'published', 'content']

    def save(self, commit=True):
        self.instance.author = self.instance.author if self.instance.pk else self.author
        return super(PostAdminForm, self).save(commit)
