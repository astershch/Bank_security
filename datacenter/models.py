from django.db import models
from django.utils.timezone import localtime
from django.utils.timezone import timedelta


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)
    boundary_time = timedelta(seconds=minutes * 60)

    is_long = duration > boundary_time

    return is_long


def get_duration(visit):
    leaved_at = localtime(visit.leaved_at)
    entered_at = localtime(visit.entered_at)

    duration = leaved_at - entered_at

    return duration


def format_duration(duration):
    timedelta_string = ''

    days = duration.days
    hours = duration.seconds // 3600
    minutes = (duration.seconds // 60) % 60

    if days:
        timedelta_string = f'{days}д '

    if hours:
        timedelta_string = f'{timedelta_string} {hours}ч '

    if minutes:
        timedelta_string = f'{timedelta_string} {minutes}м '

    if not timedelta_string:
        timedelta_string = 'Меньше минуты'

    return timedelta_string
