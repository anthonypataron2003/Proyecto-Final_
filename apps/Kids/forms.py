from django import forms
from django.contrib.auth.models import User
from apps.Kids.models import AnalisisNutricional, HistorialMedico

class LoginForm(forms.Form):
    username = forms.CharField(widget=
                               forms.TextInput(
                                   attrs={'placeholder': 'Ingrese su usuario'}))
    password = forms.CharField(widget=
                               forms.PasswordInput(
                                   attrs={'placeholder': 'Ingrese su contraseña'}))

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                              widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                               widget=forms.PasswordInput)
    class Meta:
      model = User
      fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
class AnalisisForm(forms.ModelForm):
    class Meta:
        model = AnalisisNutricional
        fields = ['imagen']
    
class HistorialForm(forms.ModelForm):
    class Meta:
        model = HistorialMedico
        fields = ['notas', 'fecha_seguimiento']
