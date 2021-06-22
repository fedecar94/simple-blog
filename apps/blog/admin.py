from django.contrib import admin

from .forms import PostAdminForm
from .models import Post, Comment


# Register your models here.


def mark_as_published(modeladmin, request, queryset):
    queryset.update(published=True)


mark_as_published.short_description = 'Show items'


def mark_as_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)


mark_as_unpublished.short_description = 'Hide items'


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    readonly_fields = ['author', 'message', 'created']

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):
    list_display = ['id', 'short_title', 'full_name', 'published']
    list_filter = ['published', 'author']
    inlines = [CommentInline]
    form = PostAdminForm
    actions = [mark_as_published, mark_as_unpublished]

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.author = request.user
        return form

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            return queryset.filter(author=request.user)
        return queryset

    def short_title(self, obj):
        return obj.title[:50] + ('...' if len(obj.title) > 50 else '.')

    short_title.short_description = 'Title'
    short_title.admin_order_field = 'title'

    def full_name(self, obj):
        return ' - '.join([str(obj.author.id), obj.author.get_full_name()])

    full_name.short_description = 'Author'
    full_name.admin_order_field = 'author'


@admin.register(Comment)
class CommentAdminModel(admin.ModelAdmin):
    list_display = ['id', 'created', 'author', 'published']
    list_filter = ['published']
    readonly_fields = ['post', 'author', 'message', 'created']
    actions = [mark_as_published, mark_as_unpublished]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            return queryset.filter(post__author=request.user)
        return queryset

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
