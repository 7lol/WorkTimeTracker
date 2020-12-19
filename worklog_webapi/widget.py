from datetime import datetime

from django.forms import DateTimeInput
from django.utils import timezone


class BootstrapDateTimePickerInput(DateTimeInput):
    template_name = 'widgets/bootstrap_datetimepicker.html'
    date_format = "%d/%m/%Y %H:%M"

    def get_context(self, name, value, attrs):
        datetimepicker_id = 'datetimepicker_{name}'.format(name=name)
        if attrs is None:
            attrs = dict()
        attrs['data-target'] = '#{id}'.format(id=datetimepicker_id)
        attrs['class'] = 'form-control datetimepicker-input'
        if value is None:
            value = timezone.now().strftime(self.date_format)
        if isinstance(value, datetime):
            value = value.strftime(self.date_format)
        context = super().get_context(name, value, attrs)
        context['widget']['datetimepicker_id'] = datetimepicker_id
        return context
