from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.core.exceptions import ObjectDoesNotExist
from api.scheduler.models import Scheduler
import datetime
import json
import uuid
from .serializers import SchedulerSerializers


registered_task = 'scheduler_task'
datetime_now = datetime.datetime.now().replace(microsecond=0)

from django.contrib.gis.geos import GEOSGeometry
def create_scheduler(aoi, product_name, start_time=datetime_now, every=1, period='minutes'):
    name = uuid.uuid4()
    kwargs_task = json.dumps({
        'product_name': product_name,
        'aoi': aoi
    })
    interval = IntervalSchedule.objects.create(every=every, period=period)
    PeriodicTask.objects.get_or_create(name=name, task=registered_task, interval=interval, start_time=start_time, kwargs=kwargs_task)
    Scheduler.objects.get_or_create(name=name, task=registered_task, start_time=start_time,
                                    every=every, period=period, aoi=GEOSGeometry(aoi), product_name=product_name)
    return {
        'Status': 'Success'
    }

def list_scheduler():
    try:
        response = SchedulerSerializers(instance=Scheduler.objects, many=True).data
        return response
    except ObjectDoesNotExist:
        return {
            'status': 'Failed',
            'message': 'Not found scheduler ' + str(id)
        }

def get_scheduler(id):
    try:
        response = SchedulerSerializers(instance=Scheduler.objects.get(pk=id), many=False).data
        return response
    except ObjectDoesNotExist:
        return {
            'status': 'Failed',
            'message': 'Not found scheduler ' + str(id)
        }

def update_scheduler(id, every=None, period=None, enabled=None):
    try:
        scheduler = Scheduler.objects.get(pk=id)
        periodic_task = PeriodicTask.objects.get(name=scheduler.name)
        interval = IntervalSchedule.objects.get(pk=periodic_task.interval_id)
        if every is not None:
            scheduler.every = every
            interval.every = every
        if period is not None:
            scheduler.period = period
            interval.period = period
        if enabled is not None:
            scheduler.enabled = enabled
            periodic_task.enabled = enabled
        periodic_task.save()
        interval.save()
        scheduler.save()
        return {
            'Status': 'Success',
            'message': 'Update scheduler successfully '
        }
    except ObjectDoesNotExist:
        return {
            'status': 'Failed',
            'message': 'Not found scheduler ' + str(id)
        }

def delete_scheduler(id):
    try:
        scheduler = Scheduler.objects.get(pk=id)
        periodic_task = PeriodicTask.objects.get(name=scheduler.name)
        interval = IntervalSchedule.objects.get(pk=periodic_task.interval_id)

        scheduler.delete()
        periodic_task.delete()
        interval.delete()
        print('I do this')
        return {
            'status': 'Success',
            'message': 'Delete Scheduler successfully'
        }

    except ObjectDoesNotExist:
        return {
            'status': 'Failed',
            'message': 'Not found scheduler ' + str(id)
        }


# TEST

from celery import task
from celery.utils.log import get_task_logger

# @task(name='get_date_now')
# def get_date_now():
#     return datetime.datetime.now()
# logger = get_task_logger(__name__)
#
# @task(name='test_scheduler')
# def test_scheduler(x):
#     time = datetime.datetime.now().replace(microsecond=0)
#     logger.info(time)
#     return x + 1000


# def create_scheduler(x, start_time=datetime_now, every=1, period='minutes'):
#     name = uuid.uuid4()
#     interval = IntervalSchedule.objects.get_or_create(every=every, period=period)
#     # time = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
#     kwargs_task = json.dumps({
#         'x': x
#     })
#     print(kwargs_task)
#     PeriodicTask.objects.get_or_create(name=name, task=registered_task, interval=interval[0], start_time=start_time, kwargs=kwargs_task)
#     # Scheduler.objects.get_or_create(name=name, task=registered_task, start_time=start_time, every=every, period=period, aoi=aoi, product_name=product_name)
#     return {
#         'Status': 'Success'
#     }


