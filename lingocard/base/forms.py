from .models import User
from django.forms import ModelForm



class UserRegisterForm(ModelForm):
    class Meta:
        model=User
        fields=['name','username','email','password']

class UserEditForm(ModelForm):
    class Meta:
        model=User
        fields=['name','username','email']