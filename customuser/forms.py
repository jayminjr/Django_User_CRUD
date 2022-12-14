from django import forms
from django.forms import widgets
from . import models


class NewUserForm(forms.ModelForm):
    class Meta:
        model = models.NewUser
        fields = ["first_name", "last_name", "email", "phone", "dob"]
        exclude = ["created_at"]
        widgets = {"dob": widgets.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        self.fields["dob"].widget.attrs[
            "placeholder"
        ] = "Formate should be '(yyyy-mm-dd)'"


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["hobbies", "age"]
        exclude = [
            "user",
        ]
        widgets = {"age": forms.HiddenInput()}


class LogInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LogInForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
