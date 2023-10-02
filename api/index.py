from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_backend.settings')

application = get_wsgi_application()

def handler(event, context):
    return WSGIHandler()(event, context)
