from .serializers import JobSerializer, CompanySerializer, CatagorySerializer, ApplicationSerializer, AccountSerializer, EducationSerializer, ResumeSerializer, WorkExperienceSerializer, AwardSerializer, SkillSerializer
from .models import Job, Company, Catagory, Application, Education, Resume, WorkExperience, Award, Skill, Account
from django.http import Http404
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .utils import token_required
from rest_framework.parsers import FormParser, MultiPartParser
from django.db.models import Count
from .models import (
    Job, Company, Catagory, Application,
    Education, Resume, WorkExperience, Award, Skill, Account
)
from .serializers import (
    JobSerializer, CompanySerializer, CatagorySerializer, ApplicationSerializer, AccountSerializer,
    EducationSerializer, ResumeSerializer, WorkExperienceSerializer, AwardSerializer, SkillSerializer
)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.kwargs.get('company_pk')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        queryset = queryset.annotate(applications_count=Count('applications'))
        return queryset

    def retrieve(self, request, pk=None, *args, **kwargs):
        job = get_object_or_404(Job, id=pk)
        serializer = JobSerializer(job, context={'request': request})
        return Response(serializer.data)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        return Company.objects.filter(user=user)

    def retrieve(self, request, pk=None):
        company = get_object_or_404(Company, id=pk)
        serializer = CompanySerializer(company, context={'request': request})
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CompanySerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class CatagoryViewSet(viewsets.ModelViewSet):
    queryset = Catagory.objects.all()
    serializer_class = CatagorySerializer

    def retrieve(self, request, pk=None):
        company = get_object_or_404(Catagory, id=pk)
        serializer = CatagorySerializer(company)
        return Response(serializer.data)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    parser_classes = (FormParser, MultiPartParser,)

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Check if a file is uploaded
        resume_file = request.FILES.get('resume')
        resume = None
        if resume_file:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Create a Resume instance without linking to a user
            resume = Resume.objects.create(
                resume=resume_file, user=request.user if request.user.is_authenticated else None)
            # Ensure resume ID is included for linking
            data['resume'] = resume.id
            data['resume_id'] = resume.id
        else:
            data.pop('resume', None)  # Remove 'resume' if not provided

        # Validate the job ID
        job_id = data.get('job')
        if job_id:
            job = get_object_or_404(Job, id=job_id)
            data['job'] = job.id

            # Prepare and validate the serializer
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                application = serializer.save()
                if request.user.is_authenticated:
                    application.user = request.user
                    application.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Invalid job ID."}, status=status.HTTP_400_BAD_REQUEST)


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(id=self.request.user.id)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def upload_files(self, request, pk=None):
        try:
            account = self.get_object()
            serializer = self.get_serializer(
                account, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"detail": "Account updated successfully."})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({"detail": f"Account with ID {pk} not found."}, status=status.HTTP_404_NOT_FOUND)


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ResumeListCreateView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        existing_resumes = Resume.objects.filter(
            user=user, title=serializer.validated_data.get('title'))
        if existing_resumes.exists():
            raise serializers.ValidationError(
                "A resume with the same title already exists.")
        serializer.save(user=user)


class ResumeDestroyView(generics.DestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
