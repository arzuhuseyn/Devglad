from django.contrib import admin
from django.contrib.auth.models import Group
from catalog.models import JobPost, Company, Tag, Representative
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

# from django.contrib.flatpages.models import FlatPage

# from catalog.forms import FlatpageCustomForm

admin.site.site_header = 'Devglad Admin'
admin.site.site_title = 'Devglad Admin'


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    search_fields = ['name']


class JobInline(admin.StackedInline):
    model = JobPost
    extra = 1
    autocomplete_fields = ['tags']
    fieldsets = (
        ("General Information", {'fields' : ('title', 'description')}),
        ("Further Information", {'fields' : ( 'is_remote', 'salary', 'required_experience')}),
        ("Tags", {'fields' : ('tags',)})
    )

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [JobInline]


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_cover_image', 'company', 'is_remote', 'salary', 'is_active')
    list_filter = ('is_remote', 'company', 'required_experience')
    list_editable = ('is_remote', 'salary', 'is_active')
    search_fields = ('title', 'company__name', 'company__location', 'tags')
    autocomplete_fields = ['tags']
    #fields = ('title', 'company', 'is_remote', 'salary', 'required_experience', 'description', 'tags')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("General Information", {'fields' : ('title', 'description')}),
        ("Cover Image", {'fields' : ('cover_image',)}),
        ("Further Information", {'fields' : ( 'is_remote', 'salary', 'required_experience')}),
        ("Tags", {'fields' : ('tags',)})
    )

    def get_cover_image(self, obj):
        if obj.cover_image:
            img = '<img src="{url}" width="200px" />'.format(url=obj.cover_image.url)
            return format_html(img)
        return format_html("<strong style='color:red;'>No Cover Image</strong>")

    get_cover_image.short_description = "Cover Image"

admin.site.register(Representative)


# admin.site.unregister(FlatPage)

# @admin.register(FlatPage)
# class FlatPageAdmin(admin.ModelAdmin):
#     form = FlatpageCustomForm
#     fieldsets = (
#         (None, {'fields': ('url', 'title', 'content', 'sites')}),
#         (_('Advanced options'), {
#             'classes': ('collapse',),
#             'fields': ('registration_required', 'template_name'),
#         }),
#     )
#     list_display = ('url', 'title')
#     list_filter = ('sites', 'registration_required')
#     search_fields = ('url', 'title')