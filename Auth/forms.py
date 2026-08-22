from django.contrib.auth.forms import UserCreationForm
from django import forms

from Auth.models import User, CollegeAdmin, CounsellorAdmin


class CustomCollegeAdminForm(UserCreationForm):
    is_staff = forms.BooleanField(
        label='Staff status',
        initial=True,
        required=False,
        disabled=True,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox'}),
    )

    class Meta:
        model = CollegeAdmin
        fields = [
            'name',
            'email',
            'mobile',
            'department',
            'designation',
            'city',
            'country',
            'state',
            'is_staff',
            'groups',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_staff'].initial = True
        self.fields['department'].required = True
        self.fields['designation'].required = True
        self.fields['city'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_college = True
        user.is_active = True
        if commit:
            user.save()
            self.save_m2m()
        return user


class ChangeCollegeAdminForm(forms.ModelForm):
    class Meta:
        model = CollegeAdmin
        fields = ['profile', 'name', 'email', 'mobile', 'dob', 'gender', 'religion', 'category', 'department',
                  'designation', 'country', 'state', 'city', 'current_address','permanent_address', 'zipcode', 'is_staff','groups']


class ChangeCounsellorAdminForm(forms.ModelForm):
    class Meta:
        model = CounsellorAdmin
        fields = ['profile', 'name', 'email', 'mobile', 'dob', 'gender', 'religion', 'category', 'brand_name',
                   'is_counsellor', 'groups']


class CustomCounsellorAdminForm(UserCreationForm):
    is_counsellor = forms.BooleanField(
        label='Counsellor Status',
        initial=True,
        required=False,
        disabled=True,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox'}),
    )

    class Meta:
        model = CounsellorAdmin
        fields = ['name', 'email', 'mobile', 'is_counsellor', 'groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_counsellor'].initial = True



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'mobile', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active','groups')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the form if needed
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['name'].widget.attrs.update({'placeholder': 'Fullname'})
        self.fields['mobile'].widget.attrs.update({'placeholder': 'Mobile Number'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
