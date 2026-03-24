from django.urls import path
from django.views.generic import RedirectView
from .views.creator_views import (
    creator_list, creator_detail, creator_create, creator_update, creator_delete,
)
from .views.library_views import (
    library_list, library_detail, library_create, library_update, library_delete,
)
from .views.song_views import (
    song_list, song_detail, song_create, song_update, song_delete,
)
from .views.generation_job_views import (
    generation_job_list, generation_job_detail, generation_job_create,
    generation_job_update, generation_job_delete,
)

urlpatterns = [
    # Home redirect
    path('', RedirectView.as_view(url='/creators/', permanent=False), name='home'),

    # Creator
    path('creators/', creator_list, name='creator_list'),
    path('creators/create/', creator_create, name='creator_create'),
    path('creators/<int:pk>/', creator_detail, name='creator_detail'),
    path('creators/<int:pk>/edit/', creator_update, name='creator_update'),
    path('creators/<int:pk>/delete/', creator_delete, name='creator_delete'),

    # Library
    path('libraries/', library_list, name='library_list'),
    path('libraries/create/', library_create, name='library_create'),
    path('libraries/<int:pk>/', library_detail, name='library_detail'),
    path('libraries/<int:pk>/edit/', library_update, name='library_update'),
    path('libraries/<int:pk>/delete/', library_delete, name='library_delete'),

    # Song
    path('songs/', song_list, name='song_list'),
    path('songs/create/', song_create, name='song_create'),
    path('songs/<int:pk>/', song_detail, name='song_detail'),
    path('songs/<int:pk>/edit/', song_update, name='song_update'),
    path('songs/<int:pk>/delete/', song_delete, name='song_delete'),

    # Generation Job
    path('jobs/', generation_job_list, name='generation_job_list'),
    path('jobs/create/', generation_job_create, name='generation_job_create'),
    path('jobs/<int:pk>/', generation_job_detail, name='generation_job_detail'),
    path('jobs/<int:pk>/edit/', generation_job_update, name='generation_job_update'),
    path('jobs/<int:pk>/delete/', generation_job_delete, name='generation_job_delete'),
]
