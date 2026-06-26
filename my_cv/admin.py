from django.contrib import admin

from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Certificate,
    Experience,
    Profile,
    Project,
    Skill,
    SkillCategory,
    SocialLink,
)


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('full_name', 'headline', 'available_for_work')


@admin.register(SocialLink)
class SocialLinkAdmin(ModelAdmin):
    list_display = ('label', 'url', 'order')
    list_editable = ('order',)


class SkillInline(TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SkillInline]


@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ('name', 'category', 'level', 'featured', 'order')
    list_editable = ('level', 'featured', 'order')
    list_filter = ('category', 'featured')
    search_fields = ('name',)


@admin.register(Experience)
class ExperienceAdmin(ModelAdmin):
    list_display = ('role', 'organization', 'period', 'is_current', 'order')
    list_editable = ('order',)
    list_filter = ('is_current',)


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ('title', 'category', 'status', 'is_featured', 'is_private', 'order')
    list_editable = ('is_featured', 'order')
    list_filter = ('category', 'status', 'is_featured', 'is_private')
    search_fields = ('title', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('skills',)


@admin.register(Certificate)
class CertificateAdmin(ModelAdmin):
    list_display = ('title', 'issuer', 'year', 'category', 'order')
    list_editable = ('order',)
    list_filter = ('category',)
    search_fields = ('title', 'issuer')
