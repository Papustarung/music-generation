from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'notification/list.html', {'notifications': notifications})
