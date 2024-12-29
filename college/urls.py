from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (AssignedStudentFaculty, AssignStudentToFacultyView,
                    ChangePassword, EnrollInSubjectView, FacultyLoginAPIView,
                    StudentCreateAPIView, StudentDetailsAPIView,
                    StudentEditAPIView, StudentLoginAPIView, SubjectListView,
                    UpdateStudentAPIView, ViewAllStudentsAPIView,
                    ViewEnrolledSubjects, create_superuser)

urlpatterns = [

    # faculty apis
    path('faculty/login/', FacultyLoginAPIView.as_view(), name='faculty-login'),
    path('student/create/', StudentCreateAPIView.as_view(), name='create-student'),
    path('students/', ViewAllStudentsAPIView.as_view(), name='view-all-students'),
    path('student/update/<int:student_id>/', UpdateStudentAPIView.as_view(), name='update-student'),
    path('assign-student/<int:student_id>/', AssignStudentToFacultyView.as_view(), name='assign-student-to-faculty'),
    path('view-enrolled-subjects/<int:student_id>/', ViewEnrolledSubjects.as_view(), name='view_enrolled_subjects'),
    path('faculty/<int:faculty_id>/students/', AssignedStudentFaculty.as_view(), name='faculty_students'),

    # student apis
    path('student/login/', StudentLoginAPIView.as_view(), name='student-login'),
    path('student/details/', StudentDetailsAPIView.as_view(), name='student-details'),
    path('student/edit/', StudentEditAPIView.as_view(), name='student-edit'),
    path('enroll-in-subject/', EnrollInSubjectView.as_view(), name='enroll-in-subject'),
    path('student/change-password/', ChangePassword.as_view(), name='change-password'),

    # subject api
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('create-superuser/', create_superuser, name='create-superuser'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





