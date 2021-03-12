from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from worklog.models import EmployeeMonth, EmployeeHoursEnrollment

import worklog_restapi.serializers


class EmployeeMonthView(ListAPIView):
    queryset = EmployeeMonth.objects.all()
    serializer_class = worklog_restapi.serializers.EmployeeMonthSerializer
    permission_classes = [IsAuthenticated]

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset.filter(employee__pk=self.request.user.employee.pk)


class EmployeeHoursEnrollmentViewSet(ListCreateAPIView):
    queryset = EmployeeHoursEnrollment.objects.all()
    serializer_class = worklog_restapi.serializers.EmployeeHoursEnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset.filter(month__pk=self.kwargs['month_id'], employee__pk=self.request.user.employee.pk)

    def perform_create(self, serializer):
        try:
            month = EmployeeMonth.objects.get(pk=self.kwargs['month_id'])
        except EmployeeMonth.DoesNotExist:
            return Response('Unauthorized', content_type="application/json", status=401)
        if month.employee != self.request.user.employee:
            return Response('Unauthorized', content_type="application/json", status=401)
        serializer.save(employee=self.request.user.employee, month=month)


class EmployeeHoursEnrollmentDetailsViewSet(ModelViewSet):
    queryset = EmployeeHoursEnrollment.objects.all()
    serializer_class = worklog_restapi.serializers.EmployeeHoursEnrollmentDetailedSerializer
    permission_classes = [IsAuthenticated]

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset.filter(employee__pk=self.request.user.employee.pk)
