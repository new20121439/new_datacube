from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


class Scheduler(models.Model):
    DAYS = 'days'
    HOURS = 'hours'
    MINUTES = 'minutes'

    PERIOD_CHOICES = (
        (DAYS, ('Days')),
        (HOURS, ('Hours')),
        (MINUTES, ('Minutes')),
    )

    name = models.CharField(
        max_length=200, unique=True,
        verbose_name=('Name'),
        help_text=('Short Description For This Task'),
        default=uuid.uuid4()

    )
    task = models.CharField(
        max_length=200,
        verbose_name='Task Name',
        help_text=('The Name of the Celery Task that Should be Run.  '
                    '(Example: "proj.tasks.import_contacts")'),
    )
    start_time = models.DateTimeField(
        blank=True, null=True,
        verbose_name=('Start Datetime'),
        help_text=(
            'Datetime when the schedule should begin '
            'triggering the task to run'),
    )
    every = models.IntegerField(
        null=False,
        verbose_name=('Number of Periods'),
        help_text=('Number of interval periods to wait before '
                    'running the task again'),
        validators=[MinValueValidator(1)],
        default=1
    )
    period = models.CharField(
        max_length=24, choices=PERIOD_CHOICES,
        verbose_name=('Interval Period'),
        help_text=('The type of period between task runs (Example: days)'),
        default=DAYS
    )
    aoi = models.GeometryField(srid=4326, geography=False)
    product_name = models.CharField(max_length=200, default=None)
    enabled = models.BooleanField(
        default=True,
        verbose_name=('Enabled'),
        help_text=('Set to False to disable the schedule'),
    )


