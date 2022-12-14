from django.urls import path, include

from . import views

app_name = "customuser"
urlpatterns = [
    path("", views.UserListView.as_view(), name="user_list"),
    path("user/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("create-user/", views.UserCreateView.as_view(), name="create_user"),
    path("update-user/<int:id>/", views.UserUpdateView.as_view(), name="update_user"),
    path("logout/", views.log_out, name="logout"),
    path("login/", views.log_in, name="login"),
]
