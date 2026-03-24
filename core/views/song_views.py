from django.shortcuts import render, get_object_or_404, redirect
from ..models import Song
from ..forms import SongForm


def song_list(request):
    songs = Song.objects.select_related('library__creator').all()
    return render(request, 'song/list.html', {'songs': songs})


def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    return render(request, 'song/detail.html', {'song': song})


def song_create(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save()
            return redirect('song_detail', pk=song.pk)
    else:
        form = SongForm()
    return render(request, 'song/form.html', {'form': form, 'title': 'Create Song'})


def song_update(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('song_detail', pk=song.pk)
    else:
        form = SongForm(instance=song)
    return render(request, 'song/form.html', {'form': form, 'title': 'Edit Song'})


def song_delete(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        song.delete()
        return redirect('song_list')
    return render(request, 'song/confirm_delete.html', {'object': song})
