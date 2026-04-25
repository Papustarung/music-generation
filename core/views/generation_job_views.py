import logging
import threading

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import GenerateSongForm, CONTENT_RULES
from ..models import GenerationJob
from ..models.enum.job_status import JobStatus
from ..notifications import notify
from ..models.entities.notification import Notification

logger = logging.getLogger(__name__)

IN_PROGRESS_STATUSES = {JobStatus.QUEUED, JobStatus.GENERATING, JobStatus.SAVING}


def _run_generation_thread(job_id: int) -> None:
    """
    Background thread target — satisfies FR-09.
    The HTTP response is returned before this finishes; generation continues
    even if the creator closes/refreshes the browser tab.
    """
    from django.db import connection
    from ..generation.service import GenerationService

    try:
        job = GenerationJob.objects.get(pk=job_id)
        GenerationService().run(job)
    except Exception:
        logger.exception("Background generation thread failed for job %s", job_id)
        GenerationJob.objects.filter(pk=job_id).update(status=JobStatus.FAILED)
    finally:
        connection.close()  # release DB connection held by the thread


@login_required
def generation_job_list(request):
    jobs = (
        GenerationJob.objects
        .filter(creator=request.user)
        .select_related('song')
        .order_by('-requested_at')
    )
    return render(request, 'generation_job/list.html', {'jobs': jobs})


@login_required
def generation_job_detail(request, pk):
    job = get_object_or_404(GenerationJob, pk=pk, creator=request.user)
    return render(request, 'generation_job/detail.html', {'job': job})


@login_required
def generation_job_create(request):
    """
    FR-05: login_required ensures only authenticated creators can access.
    FR-06: GenerateSongForm collects all required parameters.
    FR-07: form.is_valid() validates required fields before anything is created.
    FR-09: generation runs in a background thread — response returns immediately.
    """
    form = GenerateSongForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        job = GenerationJob.objects.create(
            creator=request.user,
            status=JobStatus.QUEUED,
            title=form.cleaned_data['title'],
            story=form.cleaned_data['story'],
            genre=form.cleaned_data['genre'],
            vocal_style=form.cleaned_data['vocal_style'],
            occasion=form.cleaned_data['occasion'],
            lyrics=form.cleaned_data.get('lyrics') or None,
        )

        # FR-14: tokens sufficient — notify and proceed
        notify(request.user, 'Tokens are sufficient. Your song generation has started.', Notification.Level.INFO)

        # daemon=False → thread outlives the HTTP request (FR-09)
        thread = threading.Thread(
            target=_run_generation_thread,
            args=[job.pk],
            daemon=False,
        )
        thread.start()

        return redirect('generation_job_detail', pk=job.pk)

    return render(request, 'generation_job/form.html', {
        'form': form,
        'title': 'Generate a Song',
        'show_rules': True,
        'rules': CONTENT_RULES,
    })


@login_required
def generation_job_update(request, pk):
    job = get_object_or_404(GenerationJob, pk=pk, creator=request.user)
    from ..forms import GenerationJobForm
    if request.method == 'POST':
        form = GenerationJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('generation_job_detail', pk=job.pk)
    else:
        form = GenerationJobForm(instance=job)
    return render(request, 'generation_job/form.html', {'form': form, 'title': 'Edit Job'})


@login_required
def generation_job_delete(request, pk):
    job = get_object_or_404(GenerationJob, pk=pk, creator=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('generation_job_list')
    return render(request, 'generation_job/confirm_delete.html', {'object': job})
