from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django1_app.forms import UserForm, UserProfileInfoForm


def index(request):
    return render(request, 'django1_app/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False

    if request.method == 'POST':
        # Get the data from both model forms (it appears as one form to the user on the HTML page)
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Process only if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save User Form to Database, Hash the Password, Save again with hashed password
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Save with no commit since we still need to assign to user
            profile = profile_form.save(commit=False)

            # Set one-to-one relationship between User and UserProfileInfo
            profile.user = user
            print(user)

            # Assign Profile Pic, if specified
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Save UserProfileInfo and set as Registered
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # Set the context property
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    }

    return render(request, 'django1_app/registration.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account not active')
        else:
            print('Someone tried to login and failed ')
            print(f'Username: {username} / Password: {password}')
            return HttpResponse('Login failed')
    else:
        return render(request, 'django1_app/login.html', {})


