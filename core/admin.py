from django.contrib import admin
from .models import Creator, Library, Song, GenerationJob


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'email', 'token_amount')
    search_fields = ('display_name', 'email')


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('creator',)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'vocal_style', 'occasion', 'visibility')
    list_filter = ('genre', 'vocal_style', 'occasion', 'visibility')
    search_fields = ('title',)


@admin.register(GenerationJob)
class GenerationJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'status', 'requested_at', 'title', 'genre')
    list_filter = ('status', 'genre', 'occasion')
    search_fields = ('title',)
    readonly_fields = ('requested_at',)
