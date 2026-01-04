from django.contrib import admin
import datetime

from .models import AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage, Comment
from .utilities import send_activation_notification
from .forms import SubRubricForm


@admin.action(description='Отправить письма с требованиями активации')
def send_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с требованиями отправлены')


class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли более 3 дней'),
            ('week', 'Не прошли более недели'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_activated=False, date_joined__date__lt=d)
        return queryset


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'),
              ('first_name', 'last_name'),
              ('send_messages', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_notifications,)

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(AdvUser, AdvUserAdmin)


class SubRubricInline(admin.TabularInline):
    model = SubRubric
    extra = 0


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)
    list_display = ('name', 'order')
    ordering = ('order', 'name')

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(SuperRubric, SuperRubricAdmin)


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm
    list_display = ('name', 'super_rubric', 'order')
    ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(SubRubric, SubRubricAdmin)


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('author', 'content', 'created_at', 'is_active')
    readonly_fields = ('created_at',)


class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'author', 'created_at', 'is_active')
    list_filter = ('is_active', 'rubric')
    search_fields = ('title', 'content', 'contacts')
    fields = (('rubric', 'author'), 'title', 'content', 'price', 'contacts', 'image', 'is_active')
    inlines = (AdditionalImageInline, CommentInline)

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(Bb, BbAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('bb', 'author', 'created_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('author', 'content')
    date_hierarchy = 'created_at'
    fields = ('bb', 'author', 'content', 'is_active', 'created_at')
    readonly_fields = ('created_at',)

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(Comment, CommentAdmin)