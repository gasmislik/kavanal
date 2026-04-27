from celery import shared_task
from django.db import transaction
from payment_gateway.proccess_payment import proccess_payment_simulation
from core.models import Checkout


@shared_task
def process_payment_task(data):
    try:
        result = proccess_payment_simulation(
            card_hash=data['card_hash'],
            payment_method=data['payment_method']
        )

        with transaction.atomic():
            checkout = Checkout.objects.get(id=str(data['checkout_id']))
            checkout.status_id = "e2182812-d1b0-4585-99bf-6510497602ab"
            checkout.remote_id = result
            checkout.save()

    except Exception as e:
        import logging
        logging.getLogger(__name__).exception(e)