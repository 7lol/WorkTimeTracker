import datetime

from django.contrib.auth.views import LogoutView, LoginView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from worklog_webapi.forms import EnrollmentForm
from worklog.models import Position, Month, EmployeeMonth, EmployeeHoursEnrollment, Activity, Project
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView


@login_required(login_url="/login")
def index(request):
    """View function for home page of site."""

    context = {
        'months': EmployeeMonth.get_employee_months(request.user),
        'employee': request.user.employee
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


@login_required(login_url="/login")
def employee_enrolment_list(request, *args, **kwargs):
    # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
    try:
        month = EmployeeMonth.objects.get(pk=kwargs['month_id'])
    except EmployeeMonth.DoesNotExist:
        month = None
    if not month.employee == request.user.employee:
        return HttpResponse('Unauthorized', content_type="application/json", status=401)
    if request.method == "POST":
        if 'put' in request.POST:
            form = EnrollmentForm(request.POST, user=request.user)
            if form.is_valid():
                activity_pk = form.cleaned_data['activity']
                project_pk = form.cleaned_data['project']
                newEnrollment = EmployeeHoursEnrollment.objects.create(month=EmployeeMonth.objects.get(pk=month.id),
                                                                       employee=request.user.employee,
                                                                       startDate=form.cleaned_data['start_date'],
                                                                       length=form.cleaned_data['length'],
                                                                       description=form.cleaned_data['description'],
                                                                       activity=Activity.objects.get(pk=activity_pk),
                                                                       project=Project.objects.get(pk=project_pk))
                newEnrollment.save()
            form = EnrollmentForm(user=request.user, initial={'start_date': datetime.date.today()})
        else:
            form = EnrollmentForm(request.POST, user=request.user)
    else:
        form = EnrollmentForm(user=request.user, initial={'start_date': datetime.date.today()})
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
    form_class = EnrollmentForm

    def get_form_kwargs(self):
        kwargs = super(UpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        print(self.object)
        kwargs['instance'] = self.object
        return kwargs

    def form_valid(self, form):
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

    def get_object(self, queryset=None):
        instance = super().get_object(queryset)
        return {'form': EnrollmentForm(user=self.request.user, instance=instance, block=True), 'instance': instance}

    def get_success_url(self):
        return reverse('enrollmentsList', kwargs={
            'month_id': self.object['instance'].month.pk,
        })

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.get_object()['instance'].delete()
        return HttpResponseRedirect(success_url)


class WebapiLogoutView(LogoutView):
    """
    Logout n login back
    """
    template_name = "registration/loggedout.html"


class WebapiLoginView(LoginView):
    """
    Logout n login back
    """
    template_name = "registration/login.html"
