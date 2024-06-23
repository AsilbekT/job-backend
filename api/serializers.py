from rest_framework import serializers
from .models import Job, Company, Catagory, Application, Resume
from api.models import Account
from django.urls import reverse
from django.utils import timezone
import datetime
from .models import Education, WorkExperience, Award, Skill


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'user', 'title', 'resume', 'uploaded_at']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request is None:
            raise serializers.ValidationError("Request context is required")
        validated_data['user'] = request.user
        return super().create(validated_data)


class AccountSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    resumes = ResumeSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'email',
            'username',
            'date_joined',
            'avatar',
            'last_login',
            'is_admin',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_employer',
            'resumes'
        ]


class CompanySerializer(serializers.ModelSerializer):
    company_logo = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = '__all__'

    def get_company_logo(self, obj):
        request = self.context.get('request')
        if obj.company_logo and request:
            return request.build_absolute_uri(obj.company_logo.url)
        return None


class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    destination = serializers.SerializerMethodField()
    totalSalary = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    applications_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'logo', 'job_title', 'company', 'location', 'time', 'salary', 'tag',
            'category', 'created_at', 'experience', 'job_type', 'link', 'destination', 'totalSalary', 'applications_count'
        ]

    def get_destination(self, obj):
        return obj.get_destination()

    def get_totalSalary(self, obj):
        return obj.get_total_salary()

    def get_logo(self, obj):
        request = self.context.get('request')
        logo_url = obj.company.company_logo.url
        return request.build_absolute_uri(logo_url)

    def get_link(self, obj):
        # This assumes that you have a detail view for your Company model
        return reverse('company-detail', kwargs={'pk': obj.company.pk})

    def get_created_at(self, obj):
        # This assumes that you want to show the time since the job was posted in days
        return obj.date_posted

    def get_time(self, obj):
        now = datetime.datetime.now(timezone.utc)
        # now = datetime.time(timezone.utc)
        diff = now - obj.date_posted

        hours = diff.total_seconds() // 3600
        minutes = (diff.total_seconds() % 3600) // 60

        return f"{int(hours)} hours, {int(minutes)} minutes ago"


class AccountSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    resumes = ResumeSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'email',
            'username',
            'date_joined',
            'avatar',
            'last_login',
            'is_admin',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_employer',
            'resumes'
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)
    resume_id = serializers.IntegerField(write_only=True)
    job = serializers.IntegerField(write_only=True, source='job_id')
    jobData = serializers.SerializerMethodField(read_only=True, source='job')

    class Meta:
        model = Application
        fields = ['id', 'user', 'jobData', 'resume_id', 'job', 'date_applied']
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def get_jobData(self, obj):
        return JobSerializer(obj.job, context=self.context).data

    def create(self, validated_data):
        resume_id = validated_data.pop('resume_id', None)
        job_id = validated_data.pop('job_id', None)

        if not resume_id or not job_id:
            raise serializers.ValidationError(
                "Both resume_id and job must be provided.")

        try:
            resume = Resume.objects.get(id=resume_id)
            job = Job.objects.get(id=job_id)
        except Resume.DoesNotExist:
            raise serializers.ValidationError(
                {'resume_id': "No Resume found with the given ID."})
        except Job.DoesNotExist:
            raise serializers.ValidationError(
                {'job': "No Job found with the given ID."})

        application = Application.objects.create(
            resume=resume, job=job, **validated_data)
        return application


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
