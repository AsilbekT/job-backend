from django.contrib import admin
from .models import Company, Catagory, Job, Resume, Application, Education, WorkExperience, Award, Skill


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'website', 'user')
    search_fields = ('title', 'description')
    list_filter = ('user',)


@admin.register(Catagory)
class CatagoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company', 'location',
                    'salary', 'job_type', 'date_posted')
    search_fields = ('job_title', 'company__title', 'location', 'salary')
    list_filter = ('company', 'job_type', 'date_posted')
    date_hierarchy = 'date_posted'
    ordering = ('-date_posted',)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at')
    search_fields = ('title', 'user__username')
    list_filter = ('uploaded_at',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'date_applied')
    search_fields = ('user__username', 'job__job_title')
    list_filter = ('status', 'date_applied')
    date_hierarchy = 'date_applied'
    ordering = ('-date_applied',)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_year', 'end_year', 'user')
    search_fields = ('degree', 'institution', 'user__username')
    list_filter = ('start_year', 'end_year')


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company', 'start_year', 'end_year', 'user')
    search_fields = ('job_title', 'company', 'user__username')
    list_filter = ('start_year', 'end_year')


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'user')
    search_fields = ('title', 'user__username')
    list_filter = ('year',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')
    list_filter = ('user',)
