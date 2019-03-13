from django.shortcuts import render,  redirect,get_object_or_404
from Schedule_App.forms import Login, Registration
from Schedule_App.models import User, Tutor, Student, My_Student, Schedule, Notification
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def index_page(request):
    tutors = Tutor.objects.all()
    return render(request, 'Schedule_App/index_page.html',{'tutors':tutors})


def user_login(request):
    n = request.GET.get('next')
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.user_type == 'Student':
                    login(request, user)
                    if n == '/' or n == None:
                        messages.info(request, 'Welcome to the dashboad of TRIUNE ACADEMY OF MUSIC. We are pleased to have you on board.')
                        return redirect('/profile_view/')
                    else:
                        return redirect(n)
                elif user.user_type == 'Admin' or user.user_type == 'Tutor':
                    login(request, user)
                    return redirect('/admin')
                else:
                    form = Login()
                    messages.error(request, 'It seems that you are not a registered student but a guest , please contact the administrator and enroll yourself as a student to use our services.')
                    # return render(request, 'Schedule_App/error.html')
            else:
                form = Login()
                messages.error(request, 'Invalid username or password')
                return render(request, 'Schedule_App/login.html', {'form': form})
                # return render(request, 'Schedule_App/error.html')
        else:
            form = Login()
            messages.error(request, 'Invalid username or password')
            return render(request, 'Schedule_App/login.html', {'form': form})
            # return render(request, 'Schedule_App/error.html')

    else:
        form = Login()
    return render(request, 'Schedule_App/login.html', {'form': form})


def user_register(request):
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            if password == retype_password:
                try:
                    u = User.objects.create_user(
                    username=username, password=password, email=email, first_name=first_name,
                    last_name=last_name, gender = gender,address = address,phone = phone)
                except:
                    messages.error(request,"A user with this username exist. Please choose another username")
                    return render(request, 'Schedule_App/register.html', {'form': form})
                u.save()
                messages.info(request,"Your account has been successfully created. Please log in to continue.")
                return redirect('/login/')
            else:
                messages.error(request,"Your password and retype password doesnot match!!!")
        else:
            messages.error(request,"Please enter valid details!!!")
            form = Registration()
    else:
        form = Registration()
    return render(request, 'Schedule_App/register.html', {'form': form})


@login_required
def profile_view(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'Schedule_App/profile_view.html', {'student': student})


@login_required
def profile_edit(request):
    student = Student.objects.get(user=request.user)
    if request.method == "POST":
        form = Registration(request.POST,request.FILES)
        if form.is_valid():
            student.save_data(form.cleaned_data)
            messages.success(request, 'Your profile has been successfully updated.')
            return redirect('/profile_view')
        else:
            messages.warning(request, 'Kindly use a valid data to fill up the form.')
            return render(request, 'Schedule_App/profile_edit.html', {'student': student})
    else:
        return render(request, 'Schedule_App/profile_edit.html', {'student': student})


@login_required
def schedule_my(request):
    my_st = My_Student.objects.filter(student__user=request.user)
    events = {}
    for each_my_st in my_st:
        my_list = {}
        i = 0
        schedules = Schedule.objects.filter(assignment=each_my_st.id)
        for each_schedule in schedules:
            dt = str(each_schedule.schedule).split()
            date = str(dt[0]).split("-")
            date[1] = int(date[1])-1
            date = str(str(date[0])+","+str(date[1])+","+str(date[2]))
            t = str(dt[1]).split("+")
            t = str(t[0]).split(":")
            time = str(t[0])+","+str(t[1])
            date_time = str(date)+","+str(time)
            my_list[str(i)] = date_time
            i += 1
        events[str(str(each_my_st.tutor.user.first_name)+" " +
                   str(each_my_st.tutor.user.last_name))] = my_list
    events = str(events).replace("'", '"')
    print(events)
    return render(request, 'Schedule_App/schedule_my.html', {'events': events})


@login_required
def my_tutor(request):
    tutors = Tutor.objects.filter(
        tutor_relation__student__user=request.user).distinct('id')
    print(tutors)
    return render(request, 'Schedule_App/my_tutor.html', {'tutors': tutors})


@login_required
def schedule_tutor(request,pk):
    my_st = My_Student.objects.filter(tutor__id = pk)
    events = {}
    for each_my_st in my_st:
        my_list = {}
        i = 0
        schedules = Schedule.objects.filter(assignment=each_my_st.id)
        for each_schedule in schedules:
            dt = str(each_schedule.schedule).split()
            date = str(dt[0]).split("-")
            date[1] = int(date[1])-1
            date = str(str(date[0])+","+str(date[1])+","+str(date[2]))
            t = str(dt[1]).split("+")
            t = str(t[0]).split(":")
            time = str(t[0])+","+str(t[1])
            date_time = str(date)+","+str(time)
            my_list[str(i)] = date_time
            i += 1
        events[str(str(each_my_st.student.user.first_name)+" " +
                   str(each_my_st.student.user.last_name))] = my_list
    events = str(events).replace("'", '"')
    return render(request, 'Schedule_App/schedule_tutor.html', {'events': events})


@login_required
def invoice_unpaid(request):
    return render(request, 'Schedule_App/invoice_unpaid.html')


@login_required
def invoice_paid(request):
    return render(request, 'Schedule_App/invoice_paid.html')


@login_required
def notification(request):
    st = Student.objects.get(user=request.user)
    my_st = My_Student.objects.filter(student=st)
    notifications = Notification.objects.filter(
        assignment__in=my_st).order_by('-date_time')
    return render(request, 'Schedule_App/notification.html', {'notifications': notifications})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Schedule_App/change_password.html', {
        'form': form
    })


def reset_password(request):
    return render(request, 'Schedule_App/reset_password.html')


def user_logout(request):
    messages.info(request,"You are successfully logged out. Thank you for using our services.")
    logout(request)
    return redirect('/login')
