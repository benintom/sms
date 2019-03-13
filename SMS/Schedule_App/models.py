from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.admin import UserAdmin
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    def __str__(self):
        return str(self.first_name)
    GENDER_CHOICES = (('Male', 'MALE'), ('Female', 'FEMALE'),
                      ('Other', 'OTHER'))
    USER_TYPE_CHOICES = (('Admin', 'Admin'), ('Tutor', 'Tutor'),
                         ('Student', 'Student'), ('Guest', 'Guest'))
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default='Guest')
    profile_pic = models.ImageField(
        upload_to="", blank=True, default='profile_pic.png')


class Guest(models.Model):
    def __str__(self):
        return str(self.user.first_name)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    has_booked = models.BooleanField(default=False)


class Student(models.Model):
    def __str__(self):
        return str(self.user.first_name)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    guardian_name = models.CharField(max_length=30, blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)

    def save_data(self, data):
        user = self.user
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.gender = data['gender']
        user.date_of_birth = data['date_of_birth']
        if data['profile_pic'] != None:
            user.profile_pic = data['profile_pic']
        user.address = data['address']
        user.email = data['email']
        user.phone = data['phone']
        self.guardian_name = data['guardian_name']
        self.guardian_email = data['guardian_email']
        self.guardian_phone = data['guardian_phone']
        user.save()
        self.save()


class Tutor(models.Model):
    def __str__(self):
        return str(self.user.first_name)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=20, blank=True, null=True)
    experience = models.FloatField(blank=True, null=True)
    fee_per_student = models.FloatField(blank=True, null=True)
    max_students_per_class = models.IntegerField(blank=True, null=True)


class Administrator(models.Model):
    def __str__(self):
        return str(self.user.first_name)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class My_Student(models.Model):
    def __str__(self):
        return str(str(self.tutor)+" - "+str(self.student))
    tutor = models.ForeignKey(
        Tutor, on_delete=models.CASCADE, related_name='tutor_relation')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_relation')

    class Meta:
        unique_together = ('tutor', 'student')


class Notification(models.Model):
    def __str__(self):
        return str(self.assignment)
    message = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=20, blank=True, null=True)
    date_time = models.DateTimeField(auto_now=True)
    assignment = models.ForeignKey(
        My_Student, on_delete=models.CASCADE, related_name='notification')


class Schedule(models.Model):
    def __str__(self):
        return str(self.assignment)
    schedule = models.DateTimeField(blank=True, null=True)
    date_of_booking = models.DateTimeField(auto_now=True)
    assignment = models.ForeignKey(
        My_Student, on_delete=models.CASCADE, related_name='schedule')

    class Meta:
        unique_together = ('schedule', 'assignment')
