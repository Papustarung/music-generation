from django.shortcuts import redirect, render


def home_view(request):
    if request.user.is_authenticated:
        return redirect('generation_job_create')
    return render(request, 'home.html')
