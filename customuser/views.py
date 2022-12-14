from django.views.generic import View, ListView, DetailView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from customuser.forms import LogInForm, UserInfoForm, NewUserForm
from .models import NewUser
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from .utils import get_age, get_gender_by_name, get_random_password
from django.contrib.auth import login, authenticate, logout


class UserListView(ListView):
    """
    A ListView to display all users
    """

    model = NewUser
    context_object_name = "user_list"
    template_name = "user_list.html"


class UserDetailView(DetailView):
    """
    A DetailView to display user detail
    """

    model = NewUser
    template_name = "user_detail.html"


class UserCreateView(View):
    """
    A UserCreateView to create user and userinfo.
    """

    template_name = "user_form.html"

    def get_success_url(self):
        return reverse("customuser:user_list")

    def get(self, request, *args, **kwargs):
        context = {
            "user_form": NewUserForm(),
            "user_info_form": UserInfoForm(),
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        user_form = NewUserForm(request.POST)
        user_info_form = UserInfoForm(request.POST)
        if user_form.is_valid() and user_info_form.is_valid():
            user_form.cleaned_data["gender"] = get_gender_by_name(
                user_form.cleaned_data["first_name"]
            )
            random_password = get_random_password()
            user = NewUser.objects.create_user(
                password=random_password,
                **user_form.cleaned_data,
            )
            user.save()
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.age = get_age(user.dob)
            user_info.save()
            send_mail(
                "User Created",
                f"Your user have been successfully created.\n\n Username : {user.email}\n\n Password : {random_password}",
                "from@admin.com",
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "New user created.")
            return redirect(self.get_success_url())
        else:
            context = {
                "user_form": user_form,
                "user_info_form": user_info_form,
            }
            return render(request, self.template_name, context=context)


class UserUpdateView(View):
    """
    A UserUpdateView to update user and userinfo.
    """

    template_name = "user_form.html"

    def get_success_url(self):
        return reverse("customuser:user_list")

    def get(self, request, id, *args, **kwargs):
        user = get_object_or_404(NewUser, pk=id)
        context = {
            "user_form": NewUserForm(instance=user),
            "user_info_form": UserInfoForm(instance=user.user_info),
        }
        return render(request, self.template_name, context=context)

    def post(self, request, id, *args, **kwargs):
        user = get_object_or_404(NewUser, pk=id)
        user_form = NewUserForm(request.POST, instance=user)
        user_info_form = UserInfoForm(request.POST, instance=user.user_info)
        if user_form.is_valid() and user_info_form.is_valid():
            user_form.save()
            user_info_form.save()
            messages.success(request, "User details updated.")
            return redirect(self.get_success_url())
        else:
            context = {
                "user_form": user_form,
                "user_info_form": user_info_form,
            }
            return render(request, self.template_name, context=context)


def log_out(request):
    logout(request)
    messages.success(request, "Logged out.")
    return redirect(reverse("customuser:user_list"))


def log_in(request):
    if request.user.is_authenticated:
        return redirect("customuser:user_list")
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, "Logged in.")
                return redirect("customuser:user_list")
    else:
        form = LogInForm()
    return render(request, "login.html", {"form": form})
