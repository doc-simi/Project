from django.urls import path

from django.contrib.auth import views as auth_views



urlpatterns = [
    # Password reset 
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/reset_password.html"), 
        name="reset_password"),
    
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
        name="password_reset_confirm"),
    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), 
        name="password_reset_complete"),
]
