import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import AuditLog


@login_required
def audit_log_list(request):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('hotel:dashboard')

    logs = AuditLog.objects.all().select_related('user')

    # Filter by action
    action_filter = request.GET.get('action', '')
    if action_filter and action_filter in dict(AuditLog.ACTION_CHOICES):
        logs = logs.filter(action=action_filter)

    # Filter by username
    user_filter = request.GET.get('username', '')
    if user_filter:
        import re
        if re.match(r'^[\w.\-@+]+$', user_filter):
            logs = logs.filter(username__icontains=user_filter)

    paginator = Paginator(logs, 20)
    page = request.GET.get('page', '1')
    page = page if page.isdigit() else '1'
    logs_page = paginator.get_page(int(page))

    return render(request, 'audit/audit_log_list.html', {
        'logs': logs_page,
        'action_choices': AuditLog.ACTION_CHOICES,
        'action_filter': action_filter,
        'user_filter': user_filter,
    })
