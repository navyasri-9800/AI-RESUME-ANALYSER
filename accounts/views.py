from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from .forms import RegisterForm

# Create your views here.
def home(request):
    return render(request, 'home.html')


def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('dashboard')

    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


from resumes.models import Resume
from analyzer.models import Analysis


@login_required
def dashboard(request):
    resumes_count = Resume.objects.filter(user=request.user).count()
    analyses_count = Analysis.objects.filter(resume__user=request.user).count()
    recent_analyses = Analysis.objects.filter(resume__user=request.user).order_by('-created_at')[:5]

    return render(
        request,
        'dashboard.html',
        {
            'resumes_count': resumes_count,
            'analyses_count': analyses_count,
            'recent_analyses': recent_analyses,
        }
    )


@login_required
def profile(request):
    message = None
    error = None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if email:
            request.user.email = email
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            message = "Profile updated successfully!"
        else:
            error = "Email address cannot be empty."

    resumes_count = Resume.objects.filter(user=request.user).count()
    analyses_count = Analysis.objects.filter(resume__user=request.user).count()

    return render(
        request,
        'profile.html',
        {
            'user': request.user,
            'resumes_count': resumes_count,
            'analyses_count': analyses_count,
            'message': message,
            'error': error,
        }
    )