from django.shortcuts import render, get_object_or_404, redirect
from ..models import GenerationJob
from ..forms import GenerationJobForm


def generation_job_list(request):
    jobs = GenerationJob.objects.select_related('creator', 'song').all()
    return render(request, 'generation_job/list.html', {'jobs': jobs})


def generation_job_detail(request, pk):
    job = get_object_or_404(GenerationJob, pk=pk)
    return render(request, 'generation_job/detail.html', {'job': job})


def generation_job_create(request):
    if request.method == 'POST':
        form = GenerationJobForm(request.POST)
        if form.is_valid():
            job = form.save()
            return redirect('generation_job_detail', pk=job.pk)
    else:
        form = GenerationJobForm()
    return render(request, 'generation_job/form.html', {'form': form, 'title': 'Create Generation Job'})


def generation_job_update(request, pk):
    job = get_object_or_404(GenerationJob, pk=pk)
    if request.method == 'POST':
        form = GenerationJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('generation_job_detail', pk=job.pk)
    else:
        form = GenerationJobForm(instance=job)
    return render(request, 'generation_job/form.html', {'form': form, 'title': 'Edit Generation Job'})


def generation_job_delete(request, pk):
    job = get_object_or_404(GenerationJob, pk=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('generation_job_list')
    return render(request, 'generation_job/confirm_delete.html', {'object': job})
