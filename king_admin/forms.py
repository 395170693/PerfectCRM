#__author:administrator
#date:2018/8/28
from django.utils.translation import ugettext as _
from django.forms import forms,ModelForm
from CRM import models
from django.forms import ValidationError
class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'


def create_model_form(request,admin_class):
    '''动态生成modelform'''
    def __new__(cls,*args,**kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
            if not hasattr(admin_class,"add_form"):
                 if field_name in admin_class.readonly_fields:
                     field_obj.widget.attrs['disabled'] = 'disabled'
            if hasattr(admin_class,"clean_%s" % field_name):
                field_clean_func = getattr(admin_class,"clean_%s" % field_name)
                setattr(cls,"clean_%s" % field_name,field_clean_func)
        return ModelForm.__new__(cls)
    def default_clean(self):
        '''给所有的form默认加一个clean验证'''
        print("---obj instance:",self.instance)
        error_list = []
        if self.instance.id:#代表这个是个修改的表单
            for field in admin_class.readonly_fields:
                field_val = getattr(self.instance,field)#数据库的值
                if hasattr(field_val,'select_related'):   #代表是m2m格式的
                    m2m_objs = getattr(field_val,"select_related")().select_related()
                    m2m_vals = [i[0] for i in m2m_objs.values_list('id')]
                    set_m2m_vals = set(m2m_vals)
                    set_m2m_vals_from_frontend = set([i.id for i in self.cleaned_data.get(field)])
                    if set_m2m_vals != set_m2m_vals_from_frontend:
                        # error_list.append(ValidationError(
                        #     _('Field %(field)s is readonly'),
                        #     code='invalid',
                        #     params={'field': field, }
                        # ))
                        self.add_error(field,'readonly field')
                    continue
                field_val_from_frontend = self.cleaned_data.get(field)
                #print("-----------------",field,field_val,field_val_from_frontend)
                if field_val != field_val_from_frontend:
                    error_list.append(ValidationError(
                        _('Field %(field)s is readonly,data shoud be %(val)s'),
                        code='invalid',
                        params={'field':field,'val':field_val}
                    ))
        self.ValidationError = ValidationError
        response = admin_class.default_form_validation(self)
        if response:
            error_list.append(response)
        if error_list:
            raise ValidationError(error_list)
    class Meta:
        model = admin_class.model
        fields = '__all__'
        exclude = admin_class.modelform_exculde_fields
    attrs = {'Meta':Meta,}
    _model_form_class = type('DynamicModelForm',(ModelForm,),attrs)
    setattr(_model_form_class,'__new__',__new__)
    setattr(_model_form_class,'clean',default_clean)
    # setattr(_model_form_class,'Meta',Meta)
    return _model_form_class
