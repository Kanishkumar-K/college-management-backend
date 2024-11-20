from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Subject model for list of subjects
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Faculty model -> One faculty teaches one Subject
class FacultyManager(BaseUserManager):
    def create_faculty(self, faculty_name, email, password=None, subject_name=None):
        if not email:
            raise ValueError("Faculty must have an email address")
        
        subject, created = Subject.objects.get_or_create(name=subject_name)
        
        faculty = self.model(faculty_name=faculty_name, email=self.normalize_email(email), subject=subject)
        faculty.set_password(password)
        faculty.save(using=self._db)
        return faculty

class Faculty(AbstractBaseUser):
    faculty_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name='faculty') 
    objects = FacultyManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['faculty_name', 'subject']

    def __str__(self):
        return f"{self.faculty_name} - {self.subject}"
    
    @property
    def is_authenticated(self):
        return True 

# Student model with all stduent data and foriegn keys  
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=5)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) 
    faculties = models.ManyToManyField(Faculty, related_name='students', blank=True)
    subjects = models.ManyToManyField(Subject, related_name='enrolled_students', blank=True) 
    profile_picture = models.ImageField(upload_to='profile_pics/')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_authenticated(self):
        return True