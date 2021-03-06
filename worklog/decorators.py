# Custom decorator
from django.http import HttpResponse

from worklog.models import EmployeeHoursEnrollment


def enrollment_is_yours(func):
    def check_and_call(request, *args, **kwargs):
        pk = kwargs.get("pk")
        enrollments = EmployeeHoursEnrollment.objects.filter(pk=pk)
        if len(enrollments) != 1 or not enrollments.first().employee == request.user.employee:
            return HttpResponse('Unauthorized', content_type="application/json", status=401)
        return func(request, *args, **kwargs)

    return check_and_call
