from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail

from config.celery import app


logger = get_task_logger(__name__)


@app.task(name='orders.send_order_confirmation', retry_limit=2, default_retry_delay=10, bind=10)
def send_order_confirmation(self, order_id):
    from apps.orders.models import Order
    logger.info('Notification for order:%d', order_id)
    try:
        order = Order.objects.get(id=order_id)
        send_mail('Order confirmation - {}'.format(order.get_number_display),
                  'Hi {}, thanks for your order'.format(order.full_name),
                  settings.DEFAULT_FROM_EMAIL,
                  [order.email],
                  fail_silently=False,)
    except Exception as ex:
        self.retry(exc=ex)
