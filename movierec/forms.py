from django import forms

from .models import User

class LoginForm(forms.ModelForm):
	class Meta:
		model=User
		fields = ('email','password')

class RegForm(forms.ModelForm):
	class Meta:
		model=User
		fields = ('fname','lname','email','password','sex','age','occ','pin')

class RatingsForm(forms.Form):

	rating0 = forms.IntegerField()
	rating1 = forms.IntegerField()
	rating2 = forms.IntegerField()
	rating3 = forms.IntegerField()
	rating4 = forms.IntegerField()
	rating5 = forms.IntegerField()
	rating6 = forms.IntegerField()
	rating7 = forms.IntegerField()
	rating8 = forms.IntegerField()
	rating9 = forms.IntegerField()

