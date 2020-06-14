import datetime

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.views import APIView
from rest_framework.response import Response

from WorkLog.decorators import month_is_yours
from WorkLog.forms import CreateEnrolmentForm
from WorkLog.models import Position, Month, EmployeeMonth, EmployeeHoursEnrollment, Activity, Project
from WorkLog.serializers import PositionSerializer
from rest_framework import viewsets, status
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class PositionDetail(APIView):
    """
    Get detailed position view.
    """

    def get_object(self, pk):
        try:
            return Position.objects.get(pk=pk)
        except Position.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        position = self.get_object(pk)
        serializer = PositionSerializer(position)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        position = self.get_object(pk)
        serializer = PositionSerializer(position, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        position = self.get_object(pk)
        position.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PositionList(APIView):
    """
    List all positions, or create a new position.
    """

    def get(self, request, format=None):
        positions = Position.objects.all()
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url="/accounts/login/")
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    output = []
    months = Month.objects.all()
    employee_months = EmployeeMonth.objects.filter(employee=request.user.employee)
    for length, month in enumerate(months, start=1):
        for employee_month in employee_months:
            if month == employee_month.month:
                output.append(employee_month)
                break
        if not length == len(output):
            output.append(EmployeeMonth.objects.create(month=month, employee=request.user.employee))

    context = {
        'months': output,
        'employee': request.user.employee
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


@login_required(login_url="/accounts/login/")
def employee_enrolment_list(request, pk):
    # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
    months = EmployeeMonth.objects.filter(pk=pk)
    if len(months) != 1 or not months.first().employee == request.user.employee:
        return HttpResponse('Unauthorized', content_type="application/json", status=401)
    month = months.first()
    if request.method == "POST":
        if 'put' in request.POST:
            form = CreateEnrolmentForm(request.POST, user=request.user)
            if form.is_valid():
                activity_pk = form.cleaned_data['activity']
                project_pk = form.cleaned_data['project'].id
                newEnrollment = EmployeeHoursEnrollment.objects.create(month=EmployeeMonth.objects.get(month__id=month.id),
                                                                       employee=request.user.employee,
                                                                       startDate=form.cleaned_data['start_date'],
                                                                       length=form.cleaned_data['length'],
                                                                       activity=Activity.objects.get(pk=activity_pk),
                                                                       project=Project.objects.get(pk=project_pk))
                newEnrollment.save()
            form = CreateEnrolmentForm(user=request.user, initial={'start_date': datetime.date.today()})
        else:
            form = CreateEnrolmentForm(request.POST, user=request.user)
    else:
        form = CreateEnrolmentForm(user=request.user, initial={'start_date': datetime.date.today()})
    items = EmployeeHoursEnrollment.objects.filter(month=month)
    context = {
        'form': form,
        'month': month,
        'object_list': items,
        'employee': request.user.employee
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'enrollment.html', context=context)

class EmployeeHoursEnrollmentListView(ListView):
    model = EmployeeHoursEnrollment
    template_name = 'enrollment.html'
    #form_class = CreateEnrolmentForm

    def get(self, request, *args, **kwagrs):
        # either
        self.object_list = self.get_queryset()

        month = kwagrs['month']
        self.object_list = self.object_list.filter(month=month)
        # in both cases
        context = self.get_context_data(month=month)
        return self.render_to_response(context)

    def get_queryset(self):
        return EmployeeHoursEnrollment.objects.filter(employee=self.request.user.employee)

    def get_context_data(self, **kwargs):
        employee = self.request.user.employee
        context = super().get_context_data(**kwargs)
        context['employee'] = employee
        context['month'] = kwargs['month']
        return context