from django.db import models
from django.utils.translation import ugettext_lazy as _


class TextMessage(models.Model):
    sms_body = models.CharField(_('Message content'), max_length = 170)
    caller_id = models.CharField(_('Phone number'),max_length=100, unique = False)
    sms_date = models.DateTimeField(_('Message date'))
   
    class Meta:
        verbose_name = _('Text Message')
