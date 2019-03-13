from django import forms


class Login(forms.Form):
    username = forms.CharField(label='username', max_length=20)
    password = forms.CharField(label='password', widget=forms.PasswordInput)


class Registration(forms.Form):
    username = forms.CharField(label="username", max_length=30, required=False)
    password = forms.CharField(
        label="password", widget=forms.PasswordInput, required=False)
    retype_password = forms.CharField(
        label="retype_password", widget=forms.PasswordInput, required=False)
    first_name = forms.CharField(label='first_name', max_length=30)
    last_name = forms.CharField(label='last_name', max_length=30)
    gender = forms.CharField(label='gender', max_length=10)
    date_of_birth = forms.DateField(label='date_of_birth', required=False)
    profile_pic = forms.ImageField(label='profile_pic', required=False)
    address = forms.CharField(label='address', widget=forms.Textarea)
    email = forms.EmailField(label='email')
    phone = forms.CharField(label='phone', max_length=10)
    guardian_name = forms.CharField(
        label='guardian_name', max_length=30, required=False)
    guardian_email = forms.EmailField(label='guardian_email', required=False)
    guardian_phone = forms.CharField(
        label='guardian_phone', max_length=10, required=False)
