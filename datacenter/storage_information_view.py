from datacenter.models import is_visit_long
from datacenter.models import format_duration
from datacenter.models import get_duration
from datacenter.models import Visit
from django.shortcuts import get_list_or_404
from django.shortcuts import render
from django.utils.timezone import localtime


def storage_information_view(request):
    non_closed_visits = []

    visits = get_list_or_404(Visit, leaved_at__isnull = True)

    for visit in visits:
        duration = get_duration(visit)
        is_strange = is_visit_long(visit)
        
        non_closed_visits.append(
            {
                'who_entered': visit.passcard.owner_name,
                'entered_at': localtime(visit.entered_at),
                'duration': format_duration(duration),
                'is_strange': is_strange,
            }
        )

    context = {
        'non_closed_visits': non_closed_visits,
    }

    return render(request, 'storage_information.html', context)
