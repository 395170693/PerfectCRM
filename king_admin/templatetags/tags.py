from django import template
register=template.Library()
from django.db import models
from django.utils.safestring import mark_safe




@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(obj,admin_class):
    row_ele = ''
    for column in admin_class.list_display:
        field_obj = obj._meta.get_field(column)
        if field_obj.choices:
            column_date = getattr(obj,"get_%s_display" % column)()
        else:
            column_date = getattr(obj, column)
        if type(column_date).__name__ == 'datetime':
            column_date = column_date.strftime("%Y-%m-%d %H:%M:%S")
        row_ele += "<td>%s</td>" % (column_date)
    return mark_safe(row_ele)

@register.simple_tag
def render_page_ele(loop_counter,query_sets,filter_conditions):
    filters = ''
    for k,v in filter_conditions.items():
        filters += "&%s=%s" % (k,v)
    if loop_counter < 3 or loop_counter > query_sets.paginator.num_pages -2:#代表显示前2页以及最后两页码
        ele_class = ''
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class=%s><a href="?page=%s%s">%s</a></li>''' % (ele_class,loop_counter,filters,loop_counter)
        return mark_safe(ele)

    if abs(query_sets.number - loop_counter) <= 5:
        ele_class = ''
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class=%s><a href="?page=%s%s">%s</a></li>''' % (ele_class,loop_counter,filters,loop_counter)
        return mark_safe(ele)
    return ''

@register.simple_tag
def render_filter_ele(condtion,admin_class,filter_conditions):
    # print(admin_class.model._meta.get_field(condtion))
    select_ele = "<select class='form-control' name='%s'><option value=''>请选择</option>" % condtion
    field_obj = admin_class.model._meta.get_field(condtion)
    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            if filter_conditions.get(condtion) == str(choice_item[0]):
                selected = 'selected'
            select_ele+='''<option value='%s' %s>%s</option>''' % (choice_item[0],selected,choice_item[1])
            selected =''
    if  type(field_obj).__name__ == 'ForeignKey':
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_conditions.get(condtion) == str(choice_item[0]):
                selected = 'selected'
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0],selected,choice_item[1])
            selected = ''
    select_ele += "</select>"
    return mark_safe(select_ele)


