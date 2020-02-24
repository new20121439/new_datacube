from celery.utils.log import get_task_logger
from celery import shared_task
from celery import task, chain, current_task
import time
import random


logger = get_task_logger(__name__)

@task(name='Sum_of_two_numbers')
def add(x, y):
    time.sleep(random.randint(4, 6))
    return x + y

@task(name='square_of_a_number')
def square(x):
    time.sleep(random.randint(5, 10))
    return x**2

@task(name='add_then_square')
def add_then_square(x, y):
    task = chain(
        add.s(x, y),
        square.s()
    ).apply_async()
    # result = task.get()
    # print(result + 999)
    current_task
    return task

@task(name='add_1000')
def add_1000(x):
    return x + 1000

@task(name='Combine run')
def run(x, y):
    task = chain(
        add_then_square(x, y),
        add_1000.s()
    )
    result = task.get()
    print(result + 999)
    # current_task.
    return task



# @task()
# def runFunctions(shpId, codId, stepValues, bboxTuple):
#     # ... Code to define which functions to launch ...
#     stepsToLaunch = [add_1000, add_1000, add_1000, add_1000]
#     numSteps = len(stepsToLaunch)
#
#     chainId = chain(stepsToLaunch).apply_async()
#     chainAsyncObjects = [node for node in reversed(list(nodes(chainId)))]
#
#     current_task.update_state(state="PROGRESS", meta={'step':1, 'total':numSteps})
#
#     for t in range(10800): # The same max duration of a celery task
#         for i, step in enumerate(chainAsyncObjects):
#             currStep = i+1
#             if step.state == 'PENDING':
#                 current_task.update_state(state="PROGRESS", meta={'step':currStep, 'total':numSteps})
#                 break
#             if step.state == 'SUCCESS':
#                 if currStep == numSteps:
#                     current_task.update_state(state="SUCCESS", meta={'step':currStep, 'total':numSteps})
#                     sleep(5) # Wait before stop this task, in order for javascript to get the result!
#                     return
#
#             if step.state == 'FAILURE':
#                 return
#         sleep(1)

