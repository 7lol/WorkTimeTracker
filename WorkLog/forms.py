from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _

from WorkLog.models import Activity, Project
from WorkLog.widget import BootstrapDateTimePickerInput


class CreateEnrolmentForm(forms.Form):
    start_date = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        initial=timezone.now().strftime("%d/%m/%Y %H:%M"),
        widget=BootstrapDateTimePickerInput())
    length = forms.FloatField(widget=forms.TextInput(
        attrs={'type': 'number', 'id': 'form_homework', 'min': '0.25', 'max': '8', 'step': '0.25'}))
    description = forms.CharField(max_length=256)
    activity = forms.ChoiceField()
    project = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateEnrolmentForm, self).__init__(*args, **kwargs)
        activities = user.employee.position.values("activity__name", "activity__pk").distinct()
        self.fields['activity'].choices = [[activity["activity__pk"], activity["activity__name"]] for activity in activities]
        projects = user.employee.project.all()
        self.fields['project'].choices = [[project.pk, project.name] for project in projects]
