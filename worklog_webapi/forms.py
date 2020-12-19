from datetime import datetime

from django import forms
from django.utils import timezone

from worklog.models import EmployeeHoursEnrollment
from worklog_webapi.widget import BootstrapDateTimePickerInput


class EnrollmentForm(forms.ModelForm):
    startDate = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=BootstrapDateTimePickerInput())

    class Meta:
        model = EmployeeHoursEnrollment
        length = forms.FloatField()
        description = forms.CharField(max_length=256)
        activity = forms.ChoiceField()
        project = forms.ChoiceField()
        fields = ['startDate', 'activity', 'description', 'project', 'length']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        block = kwargs.pop('block', False)
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].disabled = block
        activities = user.employee.position.values("activity__name", "activity__pk").distinct()
        self.fields['activity'].choices = [[activity["activity__pk"], activity["activity__name"]] for activity in
                                           activities]
        self.fields['length'].widget = forms.TextInput(
            attrs={'type': 'number', 'id': 'form_homework', 'max': user.employee.workingTime, 'min': '0.25',
                   'step': '0.25'})
        projects = user.employee.project.all()
        self.fields['project'].choices = [[project.pk, project.name] for project in projects]
