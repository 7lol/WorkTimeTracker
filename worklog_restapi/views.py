from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from worklog.models import Position, Employee, Month, EmployeeMonth, Project, Activity, EmployeeHoursEnrollment

# Create your views here.
from worklog_restapi.serializers import EmployeeHoursEnrollmentSerializer, EmployeeHoursEnrollmentDetailedSerializer, \
    EmployeeMonthSerializer


class EmployeeHoursEnrollmentViewSet(ListCreateAPIView):
    queryset = EmployeeHoursEnrollment.objects.all()
    serializer_class = EmployeeHoursEnrollmentSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset.filter(month__pk=self.kwargs['month_id'], employee__pk=self.request.user.employee.pk)

    def perform_create(self, serializer):
        # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
        try:
            month = EmployeeMonth.objects.get(pk=self.kwargs['month_id'])
        except EmployeeMonth.DoesNotExist:
            return Response('Unauthorized', content_type="application/json", status=401)
        if month.employee != self.request.user.employee:
            return Response('Unauthorized', content_type="application/json", status=401)
        serializer.save(employee=self.request.user.employee, month=month)


class EmployeeHoursEnrollmentDetailsViewSet(ModelViewSet):
    queryset = EmployeeHoursEnrollment.objects.all()
    serializer_class = EmployeeHoursEnrollmentDetailedSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset.filter(employee__pk=self.request.user.employee.pk)

    def perform_create(self, serializer):
        # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
        try:
            month = EmployeeMonth.objects.get(pk=self.kwargs['month_id'])
        except EmployeeMonth.DoesNotExist:
            return Response('Unauthorized', content_type="application/json", status=401)
        if month.employee != self.request.user.employee:
            return Response('Unauthorized', content_type="application/json", status=401)
        serializer.save(employee=self.request.user.employee)


class EmployeeMonthView(ListAPIView):
    queryset = EmployeeMonth.objects.all()
    serializer_class = EmployeeMonthSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset.filter(employee__pk=self.request.user.employee.pk)
