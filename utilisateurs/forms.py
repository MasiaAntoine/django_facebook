# utilisateurs/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import UtilisateurPersonnaliser


class InscriptionForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = UtilisateurPersonnaliser
		fields = ("username", "email", "telephone", "photo_profil", "est_privee", "password1", "password2")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.CheckboxInput):
				field.widget.attrs['class'] = 'form-check-input'
			else:
				field.widget.attrs['class'] = 'form-control'


class ConnexionForm(AuthenticationForm):
	username = forms.EmailField(label="Email")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'


class ProfilForm(forms.ModelForm):
	class Meta:
		model = UtilisateurPersonnaliser
		fields = ('first_name','last_name','username', 'email', 'telephone', 'photo_profil', 'ville', 'est_privee')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.CheckboxInput):
				field.widget.attrs['class'] = 'form-check-input'
			else:
				field.widget.attrs['class'] = 'form-control'


class CustomPasswordChangeForm(PasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'
