import asyncio
from datetime import timedelta

from celery import Celery

from src.repositories.admin_tasks import create_from_file, read_excel_to_data

celery = Celery('tasks')

celery.conf.update(
    broker_url='pyamqp://guest:guest@rabbitmq:5672//',
    result_backend='rpc://',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Moscow',
    enable_utc=True,
    beat_schedule={
        'main': {
            'task': 'tasks.main',
            'schedule': timedelta(seconds=15),
        },
    }
)


@celery.task
def main():
    df_menus = read_excel_to_data(menu_file='admin/Menu.xlsx')

    for menu in df_menus:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(create_from_file(menu))

    return result
