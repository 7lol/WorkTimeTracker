from django.contrib.auth.decorators import login_required
from django.urls import path, include
from worklog_webapi import views
from worklog.decorators import enrollment_is_yours

urlpatterns = [
    path('logout', views.WebapiLogoutView.as_view(), name='logout'),
    path('login', views.WebapiLoginView.as_view(), name='login'),
    path('', views.index, name='index'),
    path('month/<int:month_id>', views.employee_enrolment_list, name='enrollmentsList'),
    path('enrollment/pk=<int:pk>/month_id=<int:month_id>', enrollment_is_yours(login_required(views.EnrollmentUpdate.as_view())), name='enrollment_update'),
    path('enrollment/delete/pk=<int:pk>/month_id=<int:month_id>', enrollment_is_yours(login_required(views.EnrollmentDelete.as_view())), name='enrollment_delete'),
]