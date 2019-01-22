from django.urls import path
from django.contrib.auth.views import LoginView, TemplateView, LogoutView, PasswordResetView, PasswordResetDoneView,\
    PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeDoneView, PasswordChangeView
from . import views
from django.urls import reverse_lazy
app_name = 'accounts'

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user_list'),

    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),

    path('login/', LoginView.as_view(template_name='accounts/user-login.html'), name='login'),

    path('profile/', TemplateView.as_view(template_name='accounts/user-profile.html'), name='profile'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('AddUser/', views.CreateUserView.as_view(), name='user_signup'),

    path('UpdateUser/<int:pk>/', views.UpdateUserView.as_view(), name='user_update'),

    path('password-reset/',
         PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
                                   subject_template_name='accounts/password_reset_subject.txt',
                                   email_template_name='accounts/password_reset_email.html',
                                   success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset',),

    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',
                                          success_url=reverse_lazy('accounts:password_reset_complete')),
         name='password_reset_confirm'),

    path('reset/done/',
         PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password_change/',
         PasswordChangeView.as_view(template_name='accounts/password_change_form.html',
                                    success_url=reverse_lazy('accounts:password_change_done')), name='password_change'),

    path('password_change/done/',
         PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
]
