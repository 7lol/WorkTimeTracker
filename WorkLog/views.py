import datetime

from django.contrib.auth.views import logout_then_login, LogoutView
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from rest_framework.views import APIView
from rest_framework.response import Response

from WorkLog.forms import CreateEnrolmentForm
from WorkLog.models import Position, Month, EmployeeMonth, EmployeeHoursEnrollment, Activity, Project
from WorkLog.serializers import PositionSerializer
from rest_framework import viewsets, status
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView, DeleteView


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
def employee_enrolment_list(request, *args, **kwargs):
    # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
    months = EmployeeMonth.objects.filter(pk=kwargs['month_id'])
    if len(months) != 1 or not months.first().employee == request.user.employee:
        return HttpResponse('Unauthorized', content_type="application/json", status=401)
    month = months.first()
    if request.method == "POST":
        if 'put' in request.POST:
            form = CreateEnrolmentForm(request.POST, user=request.user)
            if form.is_valid():
                activity_pk = form.cleaned_data['activity']
                project_pk = form.cleaned_data['project']
                newEnrollment = EmployeeHoursEnrollment.objects.create(month=EmployeeMonth.objects.get(pk=month.id),
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
        'month': EmployeeMonth.objects.get(pk=month.id),
        'object_list': items,
        'employee': request.user.employee
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'enrollment.html', context=context)


class EnrollmentUpdate(UpdateView):
    model = EmployeeHoursEnrollment
    fields = ['startDate', 'activity', 'project', 'length']

    def form_valid(self, form):
        print(123)
        if len(self.request.user.employee.project.filter(pk=form.instance.project.pk)) != 1:
            form.add_error('project', 'Your not allowed to sing to this project.')
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('enrollmentsList', kwargs={
            'month_id': self.object.month.pk,
        })


class EnrollmentDelete(DeleteView):
    model = EmployeeHoursEnrollment

    def get_success_url(self):
        return reverse('enrollmentsList', kwargs={
            'month_id': self.object.month.pk,
        })


class LogoutView(LogoutView):
    """
    Logout n login back
    """
    template_name = "registration/loggedout.html"


def login(request):
    """
    Logout n login back
    """
    return login(request)