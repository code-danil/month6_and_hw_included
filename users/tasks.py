from celery import shared_task


@shared_task
def add(x, y):
    print(f'args: {x} and {y}')
    return x + y 



