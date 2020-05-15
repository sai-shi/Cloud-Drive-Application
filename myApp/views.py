from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UploadFileForm, UserRegisterForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .s3upload import *
from django.contrib import messages

# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('/')


def detail_view(request, filename):
    username = request.user.username
    filepath = '/' + username + '/media/' + filename
    response = get_from_s3('clouddrive-django-bucket', filepath)

    return response


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    username = request.user.username
    email = request.user.email
    fname = request.user.first_name
    lname = request.user.last_name
    form = PasswordChangeForm(request.POST)
    return render(request, 'profile.html', {'form': form, 'username': username, 'email': email,
                                            'first_name': fname, 'last_name': lname},)


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def handle_uploaded_file(f, username):
    uploadfilename = 'media/' + f.name
    with open(uploadfilename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    upload_to_s3_bucket_path('clouddrive-django-bucket', username, uploadfilename)
    return uploadfilename


@login_required
def delete_view(request, filename):
    username = request.user.username
    delete_from_s3('clouddrive-django-bucket', username, filename)
    userfiles, totalsize = getuserfiles('clouddrive-django-bucket', username)
    limit = 5000
    percentused = totalsize * 100 / limit
    return render(request, 'index.html', {'username': username, 'userfiles': userfiles, 'totalsize': totalsize,
                                          'limit': limit, 'percentused': percentused})


@login_required
def upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            username = request.user.username
            outputfilename = handle_uploaded_file(request.FILES['myfilefield'], username)
            userfiles, totalsize = getuserfiles('clouddrive-django-bucket', username)
            limit = 5000
            percentused = totalsize * 100 / limit
            return render(request, 'index.html', {'username': username, 'userfiles': userfiles,
                                                  'totalsize': totalsize, 'limit': limit, 'percentused': percentused})
    else:
        form = UploadFileForm()
        username = request.user.username
    return render(request, 'upload.html', {'form': form, 'username': username},)


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                username = request.user.username
                userfiles, totalsize = getuserfiles('clouddrive-django-bucket', username)
                limit = 5000
                percentused = totalsize * 100 / limit
                return render(request, 'index.html',
                                          {'username': username, 'userfiles': userfiles, 'totalsize': totalsize,
                                           'limit': limit, 'percentused': percentused},)
    else:
        if request.user.is_authenticated:
            username = request.user.username
            userfiles, totalsize = getuserfiles('clouddrive-django-bucket', username)
            limit = 5000
            percentused = totalsize * 100 / limit
            return render(request, 'index.html', {'username': username, 'userfiles': userfiles,
                                                  'totalsize': totalsize, 'limit': limit, 'percentused': percentused},)

    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def process(request):
    return render(request, 'filemanager.html', {})