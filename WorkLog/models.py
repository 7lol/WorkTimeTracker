from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.db.models import Sum

# Create your models here.
from django.dispatch import receiver


class Position(models.Model):
    name = models.CharField(max_length=64, blank=False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=False)
    surname = models.CharField(max_length=256, blank=False)
    workingTime = models.PositiveIntegerField(default=8)
    position = models.ManyToManyField(Position)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Employee.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.employee.save()

    def __str__(self):
        return '%s %s' % (self.name, self.surname)


class Month(models.Model):
    name = models.CharField(max_length=64, blank=False)
    startingDate = models.DateTimeField()
    endingDate = models.DateTimeField()
    workingDays = models.PositiveIntegerField(default=21, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['startingDate']


class EmployeeMonth(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    monthWorkingTime = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.month.name

    class Meta:
        ordering = ['month']


class Project(models.Model):
    name = models.CharField(max_length=64, blank=False)
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=64, blank=True, default='')
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EmployeeHoursEnrollment(models.Model):
    startDate = models.DateTimeField()
    length = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    description = models.CharField(max_length=256, blank=True, default='')
    month = models.ForeignKey(EmployeeMonth, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return '%s, %s, %s' % (self.employee, self.project, self.activity)

    def save(self, *args, **kwargs):
        if not self.pk:
            pass
            #self.month.monthWorkingTime = self.month.monthWorkingTime + self.length
        else:
            self.month.monthWorkingTime = EmployeeHoursEnrollment.objects.filter(month=self.month).aggregate(Sum('length'))['length__sum']
        self.month.save()
        super(EmployeeHoursEnrollment, self).save(*args, **kwargs)

    class Meta:
        ordering = ['startDate']