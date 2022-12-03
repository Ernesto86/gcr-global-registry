from django.db.models.signals import post_save
from django.dispatch import receiver

from advisers.models import Managers, PeriodCommissions, ManagersCommissions


@receiver(post_save, sender=Managers, dispatch_uid='Shopper_post_save')
def managers_post_save(sender, instance: Managers, created, **kwargs):
    if created:
        manager_id = instance.id
        period_commission = PeriodCommissions.objects.filter(deleted=False).last()

        if period_commission is None:
            raise NameError("No tiene periodo comision configurada")

        ManagersCommissions.objects.create(
            period_commissions_id=period_commission.id,
            manager_id=manager_id,
            value=period_commission.manager_percentage,
        )
