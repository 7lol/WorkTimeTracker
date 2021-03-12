from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from worklog_restapi import views

urlpatterns = [
    path('', views.EmployeeMonthView.as_view(), name='rest_index'),
    path('month/<int:month_id>', views.EmployeeHoursEnrollmentViewSet.as_view(), name='rest_enrollmentsList'),
    path('enrollment/pk=<int:pk>', views.EmployeeHoursEnrollmentDetailsViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='rest_enrollment_delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)