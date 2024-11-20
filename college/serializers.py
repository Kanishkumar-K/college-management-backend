from rest_framework import serializers
from .models import Faculty, Student, Subject

class FacultySerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Faculty
        fields = ['id', 'faculty_name', 'email', 'subject', 'subject_name'] 

class SubjectSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(many=False)  # Only one faculty per subject
    class Meta:
        model = Subject
        fields = ['id', 'name', 'faculty']
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        faculties = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all(), required=False, many=True)
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'blood_group', 'contact_number', 'address', 'email','faculties','password' ,'profile_picture']


