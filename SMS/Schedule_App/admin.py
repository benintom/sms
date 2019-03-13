from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from .models import User, Administrator, Tutor, Student, Guest, Schedule, My_Student, Notification
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('gender', 'date_of_birth',
                           'address', 'phone', 'user_type', 'profile_pic')}),
    )
    list_display = ('username', 'first_name', 'email',
                    'date_of_birth', 'gender', 'user_type')
    list_filter = ('user_type', 'is_active', 'is_staff',
                   'gender', 'date_of_birth')


class CustomAdministratorAdmin(admin.ModelAdmin):
    model = Administrator
    # list_display = ('user',)


class CustomStudent(admin.ModelAdmin):
    model = Student
    list_display = ('user', 'guardian_name',
                    'guardian_email', 'guardian_phone')
    search_fields = ('guardian_name', 'guardian_email', 'guardian_phone')


class CustomTutor(admin.ModelAdmin):
    model = Tutor
    list_display = ('user', 'subject', 'department', 'experience')
    search_fields = ('subject', 'department', 'experience')
    list_filter = ('subject', 'department')


class CustomMy_Student(admin.ModelAdmin):
    model = My_Student
    list_display = ('tutor', 'student')
    list_filter = ('tutor', 'student')


class CustomSchedule(admin.ModelAdmin):
    model = Schedule
    list_display = ('schedule', 'assignment', 'date_of_booking')
    list_filter = ('schedule', 'assignment', 'date_of_booking')


class CustomNotification(admin.ModelAdmin):
    model = Notification
    list_display = ('message', 'link', 'assignment', 'date_time')
    list_filter = ('assignment', 'date_time')
    search_fields = ('message',)


admin.site.site_header = 'Triune Admin Panel'
admin.site.register(User, CustomUserAdmin)
# admin.site.register(Administrator, CustomAdministratorAdmin)
admin.site.register(Tutor, CustomTutor)
admin.site.register(Student, CustomStudent)
# admin.site.register(Guest)
admin.site.register(My_Student, CustomMy_Student)
admin.site.register(Schedule, CustomSchedule)
admin.site.register(Notification, CustomNotification)
