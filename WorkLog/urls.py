from django.contrib.auth.decorators import login_required
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from WorkLog import views
from WorkLog.decorators import month_is_yours

urlpatterns = [
    path('', views.index, name='index'),
    path('month/<int:pk>', month_is_yours(login_required(views.EmployeeHoursEnrollmentListView.as_view())), name='enrollmentsList'),
    path('month2/<int:pk>', views.employee_enrolment_list, name='enrollmentsList2'),
    path('enrollment/<int:pk>/<int:id>', month_is_yours(login_required(views.EmployeeHoursEnrollmentListView.as_view())), name='enrollment'),
]

urlpatterns = format_suffix_patterns(urlpatterns)