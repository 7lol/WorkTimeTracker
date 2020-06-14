#Custom decorator
from django.http import HttpResponse

from WorkLog.models import EmployeeMonth


def month_is_yours(func):
    def check_and_call(request, *args, **kwargs):
        pk = kwargs.pop("pk")
        months = EmployeeMonth.objects.filter(pk=pk)
        if len(months) != 1 or not months.first().employee == request.user.employee:
            return HttpResponse('Unauthorized', content_type="application/json", status=401)
        return func(request,  month=months.first(), *args, **kwargs)
    return check_and_call