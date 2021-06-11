from django.urls import path
from django.conf import settings
from django.views.generic.base import TemplateView


from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("forgot-password", views.forgot_password, name="forgot-password"),
    path("new-task", views.newTask, name="newTask"),
    path("new-todo", views.newTodo, name="newTodo"),
    path("new-reminder", views.newReminder, name="newReminder"),
    path("task", views.viewTask, name="task"),
    path("todo", views.viewTodo, name="todo"),
    path("reminder", views.viewReminder, name="reminder"),
    path("messages", views.messages, name="messages"),
    path("notification", views.notification, name="notification"),
    path("profile", views.profile, name="profile"),
    path("settings", views.settings, name="settings"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("update", views.update, name="update"),

]
