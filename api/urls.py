from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import (
    EducationViewSet, ResumeDestroyView, ResumeListCreateView, WorkExperienceViewSet, AwardViewSet, SkillViewSet,
    JobViewSet, CompanyViewSet, CatagoryViewSet, ApplicationViewSet, AccountViewSet
)

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'catagories', CatagoryViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'user', AccountViewSet, basename='users_details')
router.register(r'education', EducationViewSet)
router.register(r'work_experience', WorkExperienceViewSet)
router.register(r'award', AwardViewSet)
router.register(r'skill', SkillViewSet)

companies_router = NestedDefaultRouter(router, r'companies', lookup='company')
companies_router.register(r'jobs', JobViewSet, basename='company-jobs')
companies_router.register(
    r'applicants', ApplicationViewSet, basename='company-applicants')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(companies_router.urls)),
    path('resumes/', ResumeListCreateView.as_view(), name='resume-list-create'),
    path('resumes/<int:pk>/', ResumeDestroyView.as_view(), name='resume-destroy'),
]
