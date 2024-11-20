import json, secrets, string, requests
from rest_framework import status
from rest_framework.exceptions import  ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .authentication import CustomFacultyJWTAuthentication
from .models import Faculty, Student, Subject
from .serializers import FacultySerializer, StudentSerializer,SubjectSerializer
from .authentication import (CustomFacultyJWTAuthentication, CustomJWTAuthentication)


# Faculty Login API View
class FacultyLoginAPIView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            faculty = Faculty.objects.get(email=email) 
        except Faculty.DoesNotExist:
            return Response({"error": "Invalid credentials. Faculty not found."}, status=status.HTTP_400_BAD_REQUEST)

        if not faculty.check_password(password):
            return Response({"error": "Invalid credentials. Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(faculty)  # JWT token
        access_token = str(refresh.access_token)

        serializer = FacultySerializer(faculty)
        return Response({
            "faculty": serializer.data,
            "access_token": access_token 
        }, status=status.HTTP_200_OK)


## Student create api  by faculty
class StudentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomFacultyJWTAuthentication] 

    def post(self, request):
        user = request.user
        if not isinstance(user, Faculty):
            return Response({"error": "Only faculty members can create student records."}, status=status.HTTP_403_FORBIDDEN)

        '''
            When a faculty creates a student record, system will generate a random password, 
            and send an email to the student with the login details.        
            Later, Student can change his/her password from the portal.

        '''
        password = self.generate_random_password() 
        profile_picture = request.FILES.get('profile_picture')

        if profile_picture and not profile_picture.content_type.startswith('image'):
            raise ValidationError('File is not an image.')

        student_data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'date_of_birth': request.data.get('date_of_birth'),
            'gender': request.data.get('gender'),
            'blood_group': request.data.get('blood_group'),
            'contact_number': request.data.get('contact_number'),
            'address': request.data.get('address'),
            'email': request.data.get('email'),
            'password': password, 
            'profile_picture': profile_picture  
        }

        serializer = StudentSerializer(data=student_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_random_password(self, length=8):
        letters = ''.join(secrets.choice(string.ascii_letters) for i in range(5))  
        digits = ''.join(secrets.choice(string.digits) for i in range(2)) 
        special_char = secrets.choice(string.punctuation)  
        
        password = letters + digits + special_char
        password_list = list(password)
        secrets.SystemRandom().shuffle(password_list) 
        return ''.join(password_list)


## View all students
class ViewAllStudentsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomFacultyJWTAuthentication] 

    def get(self, request):
        user = request.user
        if not isinstance(user, Faculty):
            return Response({"error": "Only faculty members can view student records."}, status=status.HTTP_403_FORBIDDEN)

        students = Student.objects.all()
        student_data = [
                {
                    "id": student.id,
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "date_of_birth": student.date_of_birth,
                    "gender": student.gender,
                    "blood_group": student.blood_group,
                    "contact_number": student.contact_number,
                    "address": student.address,
                    "email": student.email,
                }
                for student in students
            ]
        return Response(student_data, status=status.HTTP_200_OK)

# Update stduent data by id
class UpdateStudentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomFacultyJWTAuthentication]  

    def put(self, request, student_id):
        user = request.user
        if not isinstance(user, Faculty):
            return Response({"error": "Only faculty members can update student records."}, status=status.HTTP_403_FORBIDDEN)

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        student_data = {
            'first_name': request.data.get('first_name', student.first_name),
            'last_name': request.data.get('last_name', student.last_name),
            'date_of_birth': request.data.get('date_of_birth', student.date_of_birth),
            'gender': request.data.get('gender', student.gender),
            'blood_group': request.data.get('blood_group', student.blood_group),
            'contact_number': request.data.get('contact_number', student.contact_number),
            'address': request.data.get('address', student.address),
        }

        serializer = StudentSerializer(student, data=student_data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Student login
class StudentLoginAPIView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            return Response({"error": "Invalid credentials. Student not found."}, status=status.HTTP_400_BAD_REQUEST)

        if student.password != password:  
            return Response({"error": "Invalid credentials. Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(student)
        access_token = str(refresh.access_token)

        serializer = StudentSerializer(student)

        return Response({
            "student": serializer.data,
            "access_token": access_token  
        }, status=status.HTTP_200_OK)

# Stduent details view
class StudentDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]  

    def get(self, request):
        student = request.user  

        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Student data edit
class StudentEditAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]  

    def put(self, request):
        student = request.user  
        allowed_fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'blood_group', 'contact_number', 'address', 'profile_picture']
        
        data_to_update = {field: request.data.get(field) for field in allowed_fields if field in request.data}

        serializer = StudentSerializer(student, data=data_to_update, partial=True) 
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Assign student to faculty
class AssignStudentToFacultyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomFacultyJWTAuthentication]

    def post(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        faculty = request.user 

        if not isinstance(faculty, Faculty):
            return Response({"error": "Only loggedin faculty can assign student to himself."}, status=status.HTTP_400_BAD_REQUEST)

        student.faculties.add(faculty)

        student.save()
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

# View Assigned Students to faculty
class AssignedStudentFaculty(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request, faculty_id):
        try:
            faculty = Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return Response({"error": "Faculty not found"}, status=404)
        
        students = faculty.students.all()
        student_ids = [student.id for student in students]
        return Response({"faculty_id": faculty_id, "student_ids": student_ids})


# Enrol in subjects by student
class EnrollInSubjectView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]  

    def post(self, request):
        student = request.user  
        subject_names = request.data.get("subjects", [])
        subjects = []
        
        for name in subject_names:
            try:
                subject = Subject.objects.get(name=name)
                subjects.append(subject)
            except Subject.DoesNotExist:
                return Response({"error": f"Subject '{name}' not found"}, status=status.HTTP_404_NOT_FOUND)
        
        student.subjects.add(*subjects)        
        return Response({"message": "Enrolled in subjects successfully"}, status=status.HTTP_200_OK)

# View enrolled subjects
class ViewEnrolledSubjects(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]  

    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        subjects = student.subjects.all()  
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Password Change
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[CustomJWTAuthentication]

    def patch(self, request):
        if 'password' not in request.data or 'new_password' not in request.data:
            return Response({"error": "Please provide both old and new password"}, status=status.HTTP_400_BAD_REQUEST)

        old_password = request.data.get('password')
        new_password = request.data.get('new_password')
        user = request.user 
        if user.password != old_password: 
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.password = new_password 
        user.save()

        return Response({"message": "Password successfully updated"}, status=status.HTTP_200_OK)

# View all subjects
class SubjectListView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


