from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, \
                                      PasswordResetConfirmView
from account.forms import User_Registration_Form, UserEditForm

def register(request):
    if request.method == 'POST':
        form = User_Registration_Form(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'account/register_done.xhtml', {'newuser': new_user })
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_message = f"Error in {field}: {error}"
                    error_messages.append(error_message)

            # Add a message to notify the user
            for error_message in error_messages:
                messages.error(request, error_message)
    else:
        form = User_Registration_Form()    
    return render(request, 'account/register.xhtml', {'form': form })

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Account updated '\
                                      'successfully')
        else:
            error_messages = []
            for field, errors in user_form.errors.items():
                for error in errors:
                    error_message = f"Error in {field}: {error}"
                    error_messages.append(error_message)

            # Add a message to notify the user
            for error_message in error_messages:
                messages.error(request, error_message)
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request,
                  'account/edit.xhtml',
                  {'user_form': user_form})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    paginator = Paginator(users, 4)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,
                  'account/user/list.xhtml',
                  {'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.xhtml',
                  {'user': user})

def test(request):
    return render(request, 'registration/logged_out.html')


class CustomPasswordChangeView(PasswordChangeView):

    def get_success_url(self):
        # Specify the URL to redirect to after a successful password change
        return reverse('account:password_change_done')
    
# CBV
class CustomPasswordResetView(PasswordResetView):

    def get_success_url(self):
        return reverse('account:password_reset_done')
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):

    def get_success_url(self):
        return reverse('account:password_reset_complete')
    