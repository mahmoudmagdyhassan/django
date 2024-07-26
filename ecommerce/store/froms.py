from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserCreationForms(UserCreationForm):
    username = forms.CharField(label='username')
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput())

    # Override save method to set password without validation
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # تعيين كلمة المرور دون فحص
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')








class Login_Form(forms.ModelForm):
    username = forms.CharField(
        max_length=63,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ('username','password')
