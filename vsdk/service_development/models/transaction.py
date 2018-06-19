from django.db import models
from django.utils.translation import ugettext_lazy as _

class Transaction(models.Model):
    INCOMING = 'IN'
    OUTGOING = 'OUT'
    customer_name = models.CharField(_('Customer name'), max_length = 100)
    id = models.CharField(_('Tansaction ID'), max_length = 100, primary_key = True)
    date = models.CharField(_('Transaction date'), max_length = 100)
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    reference = models.CharField(_('Reference'), max_length = 100, null = True)

    TYPE_OF_TRANSACTION = ((INCOMING, 'incoming'), (OUTGOING, 'outgoing'))
    transaction_type = models.CharField(_('Tansaction type'), max_length=2, choices = TYPE_OF_TRANSACTION, default=INCOMING)


    class Meta:
        verbose_name = _('Transaction')
    
