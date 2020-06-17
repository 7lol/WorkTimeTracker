from rest_framework import serializers


'''
    EXAMPLE USAGE:
        def filter_employee(self, queryset):
            request = self.context['request']
            return queryset.filter(user=request.user.employee)
'''

class FilterRelatedMixin(object):
    def __init__(self, *args, **kwargs):
        super(FilterRelatedMixin, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, serializers.RelatedField):
                method_name = 'filter_%s' % name
                try:
                    func = getattr(self, method_name)
                except AttributeError:
                    pass
                else:
                    field.queryset = func(field.queryset)