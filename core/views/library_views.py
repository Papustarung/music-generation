from django.shortcuts import render, get_object_or_404, redirect
from ..models import Library
from ..forms import LibraryForm


def library_list(request):
    libraries = Library.objects.select_related('creator').all()
    return render(request, 'library/list.html', {'libraries': libraries})


def library_detail(request, pk):
    library = get_object_or_404(Library, pk=pk)
    return render(request, 'library/detail.html', {'library': library})


def library_create(request):
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            library = form.save()
            return redirect('library_detail', pk=library.pk)
    else:
        form = LibraryForm()
    return render(request, 'library/form.html', {'form': form, 'title': 'Create Library'})


def library_update(request, pk):
    library = get_object_or_404(Library, pk=pk)
    if request.method == 'POST':
        form = LibraryForm(request.POST, instance=library)
        if form.is_valid():
            form.save()
            return redirect('library_detail', pk=library.pk)
    else:
        form = LibraryForm(instance=library)
    return render(request, 'library/form.html', {'form': form, 'title': 'Edit Library'})


def library_delete(request, pk):
    library = get_object_or_404(Library, pk=pk)
    if request.method == 'POST':
        library.delete()
        return redirect('library_list')
    return render(request, 'library/confirm_delete.html', {'object': library})
