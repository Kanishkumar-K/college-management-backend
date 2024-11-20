from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Student, Faculty

# for students
class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            return Student.objects.get(id=user_id)
        except Student.DoesNotExist:
            raise AuthenticationFailed("Student not found.")

# for faculty
class CustomFacultyJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            return Faculty.objects.get(id=user_id)
        except Faculty.DoesNotExist:
            raise AuthenticationFailed("Faculty not found.")
