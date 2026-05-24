from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter email address',
            'class': 'w-full bg-white/5 border border-white/10 rounded-xl pl-11 pr-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-violet-500 transition-colors'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'First name',
            'class': 'w-full bg-white/5 border border-white/10 rounded-xl pl-11 pr-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-violet-500 transition-colors'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'Last name',
            'class': 'w-full bg-white/5 border border-white/10 rounded-xl pl-11 pr-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-violet-500 transition-colors'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply premium styling to username and password fields
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Choose username',
            'class': 'w-full bg-white/5 border border-white/10 rounded-xl pl-11 pr-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-violet-500 transition-colors'
        })
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'placeholder': 'Enter password',
                'class': 'w-full bg-white/5 border border-white/10 rounded-xl pl-11 pr-10 py-3 text-sm text-slate-200 focus:outline-none focus:border-violet-500 transition-colors'
            })
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'placeholder': 'Confirm password',
                'class': 'w-full bg-white/5 border border-white/10 rounded-xl pl-11 pr-10 py-3 text-sm text-slate-200 focus:outline-none focus:border-violet-500 transition-colors'
            })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email
