# College Management System Backend

This project is a backend implementation for a College Management System using Django REST Framework (DRF). It supports role-based access for faculties and students, allowing efficient management of user data, authentication, and subjects.

---

## Features

| **Feature**                    | **Description**                                                                                   |
|--------------------------------|---------------------------------------------------------------------------------------------------|
| **Faculty Login**              | Faculty can log in using email and password to access the system.                                |
| **Student Management**         | Faculty can create, view, update, and assign students.                                           |
| **Student Login**              | Students can log in using email and password to manage their profiles.                           |
| **Subjects Management**        | Students can enroll in subjects; faculty can manage subject assignments.                        |
| **Password Management**        | Both faculty and students can change passwords securely.                                         |
| **Role-based Access**          | Access control enforced for faculty and student actions via custom JWT authentication.           |

---

## Models Overview

| **Model**    | **Fields**                                                                                          |
|--------------|----------------------------------------------------------------------------------------------------|
| **Faculty**  | `faculty_name`, `email`, `password`, `subject`                       |
| **Student**  | `first_name`, `last_name`, `date_of_birth`, `gender`, `blood_group`, `contact_number`, `email`      |
| **Subject**  | `name`                                                          |

---

## API Endpoints

### Faculty APIs

| **Endpoint**             | **Method** | **Description**                               |
|--------------------------|------------|-----------------------------------------------|
| `/faculty/login`         | POST       | Login for faculty members.                   |
| `/faculty/students/`     | GET        | View all students.                           |
| `/faculty/students/`     | POST       | Create a new student record.                 |
| `/faculty/students/:id`  | PUT        | Update student details by ID.                |
| `/faculty/assign/:id`    | POST       | Assign a student to a faculty.               |

### Student APIs

| **Endpoint**             | **Method** | **Description**                               |
|--------------------------|------------|-----------------------------------------------|
| `/student/login`         | POST       | Login for students.                          |
| `/student/details/`      | GET        | View logged-in student details.              |
| `/student/edit/`         | PUT        | Edit student profile.                        |
| `/student/subjects/`     | POST       | Enroll in subjects.                          |
| `/student/subjects/:id`  | GET        | View enrolled subjects by student ID.        |

### Miscellaneous APIs

| **Endpoint**             | **Method** | **Description**                               |
|--------------------------|------------|-----------------------------------------------|
| `/subjects/`             | GET        | List all subjects.                           |
| `/password/change`       | PATCH      | Change user password.                        |
| `/admin/create`          | GET        | Create a predefined superuser (admin).       |

---


## Installation and Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd college-management-backend
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Apply Migrations
Run the migrations to set up the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Start the Development Server
Start the development server to run the application locally:

```bash
python manage.py runserver
```
