from django.urls import path
from .views.home_view import home_view
from .views.auth_views import (
    login_view, register_view, logout_view,
    google_redirect_view, google_callback_view,
)
from .views.creator_views import (
    creator_list, creator_detail, creator_create, creator_update, creator_delete,
)
from .views.song_views import (
    song_list, song_detail, song_update, song_delete, shared_song, song_download, song_stream,
)
from .views.generation_job_views import (
    generation_job_list, generation_job_detail, generation_job_create,
    generation_job_update, generation_job_delete,
)
from .views.webhook_views import suno_webhook
from .views.notification_views import notification_list

urlpatterns = [
    # Home
    path('', home_view, name='home'),

    # Auth
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/google/', google_redirect_view, name='google_redirect'),
    path('auth/google/callback/', google_callback_view, name='google_callback'),

    # Creator (admin-style management)
    path('creators/', creator_list, name='creator_list'),
    path('creators/create/', creator_create, name='creator_create'),
    path('creators/<int:pk>/', creator_detail, name='creator_detail'),
    path('creators/<int:pk>/edit/', creator_update, name='creator_update'),
    path('creators/<int:pk>/delete/', creator_delete, name='creator_delete'),

    # Public shared song — no auth required (FR-31/FR-32/FR-33)
    path('songs/shared/<uuid:token>/', shared_song, name='shared_song'),

    # Library — FR-17: personal library of songs (read + manage songs only)
    path('songs/', song_list, name='song_list'),
    path('songs/<int:pk>/', song_detail, name='song_detail'),
    path('songs/<int:pk>/edit/', song_update, name='song_update'),
    path('songs/<int:pk>/delete/', song_delete, name='song_delete'),
    path('songs/<int:pk>/download/', song_download, name='song_download'),
    path('songs/<int:pk>/stream/', song_stream, name='song_stream'),

    path('notifications/', notification_list, name='notification_list'),

    # Suno webhook (no auth — external callback)
    path('jobs/webhook/suno/', suno_webhook, name='suno_webhook'),

    # Generation Job
    path('jobs/', generation_job_list, name='generation_job_list'),
    path('jobs/create/', generation_job_create, name='generation_job_create'),
    path('jobs/<int:pk>/', generation_job_detail, name='generation_job_detail'),
    path('jobs/<int:pk>/edit/', generation_job_update, name='generation_job_update'),
    path('jobs/<int:pk>/delete/', generation_job_delete, name='generation_job_delete'),
]
