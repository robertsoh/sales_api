# coding: utf-8
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Item


@receiver(post_save, sender=Item)
def post_save_item(sender, instance, **kwargs):
    instance.order.compute_total()
    instance.order.save()


@receiver(post_delete, sender=Item)
def post_delete_item(sender, instance, **kwargs):
    instance.order.compute_total()
    instance.order.save()
