from rest_framework import serializers

from worklog.models import Month, Project, Activity, EmployeeHoursEnrollment, EmployeeMonth


class MonthSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Month
        fields = ['name', 'startingDate', 'endingDate', 'workingDays']
        lookup_field = None


class EmployeeMonthSerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='rest_enrollmentsList', format='html', lookup_field='pk',
                                                lookup_url_kwarg='month_id', read_only=True)
    month = MonthSerializer()

    class Meta:
        model = EmployeeMonth
        fields = ['id', 'link', 'month', 'monthWorkingTime']
        lookup_field = None


class EmployeeHoursEnrollmentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='rest_enrollment_delete', format='html')
    activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects)

    class Meta:
        model = EmployeeHoursEnrollment
        fields = ['id', 'startDate', 'length', 'activity', 'description', 'project']
        lookup_field = None

    def __init__(self, *args, **kwargs):
        super(EmployeeHoursEnrollmentSerializer, self).__init__(*args, **kwargs)
        request = self.context['request']
        activities = Activity.objects.filter(position__in=request.user.employee.position.all())
        self.fields['activity'].queryset = activities
        self.fields['project'].queryset = request.user.employee.project


class EmployeeHoursEnrollmentDetailedSerializer(serializers.HyperlinkedModelSerializer):
    activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects)
    month = serializers.PrimaryKeyRelatedField(queryset=EmployeeMonth.objects)

    class Meta:
        model = EmployeeHoursEnrollment
        fields = ['id', 'startDate', 'length', 'activity', 'description', 'month', 'project']
        lookup_field = None

    def __init__(self, *args, **kwargs):
        super(EmployeeHoursEnrollmentDetailedSerializer, self).__init__(*args, **kwargs)
        request = self.context['request']
        activities = Activity.objects.filter(position__in=request.user.employee.position.all())
        self.fields['activity'].queryset = activities
        self.fields['project'].queryset = request.user.employee.project
        self.fields['month'].queryset = EmployeeMonth.objects.filter(employee__pk=request.user.employee.pk)
