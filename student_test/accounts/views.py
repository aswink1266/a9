from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView, ListView


class CreateUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View for creating admin,staffs & students
    , which is done by the staffs with admin privileges.
    """
    model = User
    template_name = 'accounts/user-signup.html'
    success_url = reverse_lazy('accounts:user_signup')
    fields = ['first_name', 'last_name', 'username', 'email', 'password', 'is_superuser', 'is_staff']

    def test_func(self):
        """
        :return: Returns only if the user is admin .
        """
        return self.request.user.is_superuser

    def form_valid(self, form):
        """
        Function for overriding the form and saving it.
        :param form: Saving the user sign up form .
        :return: Returns to the success page.
        """
        User.objects.create_user(**form.cleaned_data)
        return redirect(self.success_url)


class UserDetail(DetailView):
    """
    View for showing the detail details.
    """
    model = User
    template_name = 'accounts/user-detail.html'
    context_object_name = 'user_profile'


class UserList(ListView):
    """
    View for showing the list of users.
    """
    model = User
    template_name = 'accounts/user-list.html'
    context_object_name = 'users'

    def get_queryset(self):
        """
        Function for overriding queryset to get filtered data .
        :return: returns the data available in the list.
        """
        queryset = User.objects.all()

        term = self.request.GET.get('term')
        if term:
            queryset = queryset.filter(Q(first_name__icontains=term) | Q(last_name__contains=term))

        return queryset


class UpdateUserView(UpdateView):
    """
    View for updating the user details.
    """
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'is_superuser', 'is_staff']
    template_name = 'accounts/user-update.html'
    success_url = reverse_lazy('accounts:user_list')


class Index(TemplateView):
    """
    View for showing the index of the application
    """
    model = User
    template_name = 'accounts/index.html'
