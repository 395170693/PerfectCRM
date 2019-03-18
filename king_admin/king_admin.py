from CRM import models

enabled_admins = {}


class BaseAdmin(object):
    list_display = [],
    list_filters = []
    search_fields = []
    list_per_page = 5
    ordering = None
    filter_horizontal = []
    modelform_exculde_fields = []
    def default_form_validation(self):
        '''用户可以在这里自定义表单验证，相当于django form的clean方法'''
        pass

class CustomerAdmin(BaseAdmin):
    list_display = ['id', 'qq', 'name', 'source', 'consultant', 'date', 'consult_course', 'status','enroll']
    list_filters = ['source', 'consultant', 'consult_course', 'status', 'date']
    list_per_page = 5
    search_fields = ['qq', 'name', 'consultant__name']
    filter_horizontal = ['tags']
    readonly_fields=['qq',"consultant",'tags']
    modelform_exculde_fields = []
    def enroll(self):
        return '''<a href="/crm/customer/%s/enrollment/">报名</a>''' % self.instance.id
    enroll.display_name = "报名链接"
    def default_form_validation(self):
        consult_content = self.cleaned_data.get("content")
        if len(consult_content) < 15:
            return self.ValidationError(
                    ('Field %(field)s 咨询内容记录不能少于15个字符!'),
                    code='invalid',
                    params={'field': 'content'}
            )
    def clean_name(self):
        #print("name-------------------",self.cleaned_data['name'])
        if not self.cleaned_data['name']:
            self.add_error('name','不能为空')



class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer', 'consultant', 'date')

class UserProfileAdmin(BaseAdmin):
    list_display = ('email','name')
    readonly_fields = ('password',)
    modelform_exculde_fields = ['last_login',]
    filter_horizontal = ('user_permissions','groups')


def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}

    admin_class.model = model_class
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)
register(models.UserProfile, UserProfileAdmin)