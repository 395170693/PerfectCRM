


from CRM import models
enabled_admins = {}
class BaseAdmin(object):
    list_display = []
    list_filters = []


class CustomerAdmin(BaseAdmin):
    list_display = ['qq','name','source','consultant','date','consult_course','status']
    list_filters = ['source','consultant','consult_course','status']
    list_per_page = 1
class CustomerFollowUpAdmin(BaseAdmin):
    list_per_page = 1
    list_display = ('customer','consultant','date')

def register(model_class,admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}

    admin_class.model = model_class
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class

register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)