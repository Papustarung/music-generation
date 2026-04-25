from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from django.db.models.signals import post_save
        from django.dispatch import receiver
        from .models.entities.creator import Creator
        from .models.entities.library import Library

        @receiver(post_save, sender=Creator)
        def create_library_for_creator(sender, instance, created, **kwargs):
            if created:
                Library.objects.get_or_create(creator=instance)
