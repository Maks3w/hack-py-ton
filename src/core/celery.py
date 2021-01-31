from celery import Celery, signals
from django.conf import settings


app = Celery('core')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # noqa: T001


@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    pass
