from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Song
from ..forms import SongForm
from ..models.enum.visibility import Visibility


@login_required
def song_list(request):
    """FR-16/FR-17/FR-18: Show only the signed-in creator's songs."""
    songs = (
        Song.objects
        .filter(library__creator=request.user)
        .order_by('-id')
    )
    return render(request, 'song/list.html', {'songs': songs})


@login_required
def song_detail(request, pk):
    """FR-16/FR-19: Open a song — restricted to its owner."""
    song = get_object_or_404(Song, pk=pk, library__creator=request.user)
    return render(request, 'song/detail.html', {'song': song})


@login_required
def song_update(request, pk):
    """Allow creator to toggle visibility or edit metadata (FR-18)."""
    song = get_object_or_404(Song, pk=pk, library__creator=request.user)
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('song_detail', pk=song.pk)
    else:
        form = SongForm(instance=song)
    return render(request, 'song/form.html', {'form': form, 'title': 'Edit Song'})


def shared_song(request, token):
    """FR-31 / FR-32 / FR-33: Public shared song — no login required."""
    song = get_object_or_404(Song, share_token=token)
    if song.visibility != Visibility.SHARED:
        return render(request, 'song/shared_unavailable.html', status=403)
    return render(request, 'song/shared.html', {'song': song})


@login_required
def song_delete(request, pk):
    """FR-20: Delete a song from the library."""
    song = get_object_or_404(Song, pk=pk, library__creator=request.user)
    if request.method == 'POST':
        song.delete()
        return redirect('song_list')
    return render(request, 'song/confirm_delete.html', {'object': song})

