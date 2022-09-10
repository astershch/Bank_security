from datacenter.models import is_visit_long
from datacenter.models import get_duration
from datacenter.models import format_duration
from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.shortcuts import render
from django.utils.timezone import localtime


def passcard_info_view(request, passcode):
    this_passcard_visits = []

    visits = get_list_or_404(Visit, passcard__passcode=passcode)
    passcard = get_object_or_404(Passcard, passcode=passcode)

    for visit in visits:
        duration = get_duration(visit)
        is_strange = is_visit_long(visit)

        this_passcard_visits.append(
            {
                'entered_at': localtime(visit.entered_at),
                'duration': format_duration(duration),
                'is_strange': is_strange,
            }
        )
    
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits,
    }
    
    return render(request, 'passcard_info.html', context)
