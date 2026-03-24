from django.shortcuts import render, get_object_or_404, redirect
from ..models import Creator
from ..forms import CreatorForm


def creator_list(request):
    creators = Creator.objects.all()
    return render(request, 'creator/list.html', {'creators': creators})


def creator_detail(request, pk):
    creator = get_object_or_404(Creator, pk=pk)
    return render(request, 'creator/detail.html', {'creator': creator})


def creator_create(request):
    if request.method == 'POST':
        form = CreatorForm(request.POST)
        if form.is_valid():
            creator = form.save()
            return redirect('creator_detail', pk=creator.pk)
    else:
        form = CreatorForm()
    return render(request, 'creator/form.html', {'form': form, 'title': 'Create Creator'})


def creator_update(request, pk):
    creator = get_object_or_404(Creator, pk=pk)
    if request.method == 'POST':
        form = CreatorForm(request.POST, instance=creator)
        if form.is_valid():
            form.save()
            return redirect('creator_detail', pk=creator.pk)
    else:
        form = CreatorForm(instance=creator)
    return render(request, 'creator/form.html', {'form': form, 'title': 'Edit Creator'})


def creator_delete(request, pk):
    creator = get_object_or_404(Creator, pk=pk)
    if request.method == 'POST':
        creator.delete()
        return redirect('creator_list')
    return render(request, 'creator/confirm_delete.html', {'object': creator})
