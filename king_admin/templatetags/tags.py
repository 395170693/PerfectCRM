from django import template
register=template.Library()
from django.db import models
from django.utils.timezone import datetime,timedelta#导入时区相关时间
from django.utils.safestring import mark_safe
from django.core.exceptions import FieldDoesNotExist



@register.simple_tag
def render_app_name(admin_class):
    print(admin_class.model._meta.verbose_name)
    return admin_class.model._meta.verbose_name


@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(request,obj,admin_class):
    row_ele = ''
    for index,column in enumerate(admin_class.list_display):
        try:
            field_obj = obj._meta.get_field(column)
            if field_obj.choices:
                column_data = getattr(obj,"get_%s_display" % column)()
            else:
                column_data = getattr(obj, column)
            if type(column_data).__name__ == 'datetime':
                column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")
            if index == 0:#添加a标签，可以跳转到修改页码
                column_data = "<a href='{request_path}{obj_id}/change/'>{data}</a>".format(request_path=request.path,
                                                                                            obj_id = obj.id,
                                                                                            data = column_data,
                                                                                            )
        except FieldDoesNotExist as e:
            if hasattr(admin_class,column):
                column_func = getattr(admin_class,column)
                admin_class.instance = obj
                admin_class.request = request
                column_data = column_func()

        row_ele += "<td>%s</td>" % (column_data)
    return mark_safe(row_ele)

@register.simple_tag
def build_paginators(query_sets,filter_conditions,previous_orderby,search_text):
    page_btns= ''
    filters = ''
    for k, v in filter_conditions.items():
        filters += "&%s=%s" % (k, v)
    added_dot_ele = False
    for page_num in query_sets.paginator.page_range:
        if page_num < 3 or page_num > query_sets.paginator.num_pages -2 or \
                abs(query_sets.number - page_num) <= 1:#代表最前两页或者最后两页
            ele_class = ''
            if query_sets.number == page_num:
                added_dot_ele = False
                ele_class = "active"
            page_btns += '''<li class=%s><a href="?page=%s%s&o=%s&_q=%s">%s</a></li>''' %(
            ele_class, page_num, filters,previous_orderby,search_text,page_num)
        else:  # 显示...
            if added_dot_ele == False:
                page_btns += '<li><a>...</a></li>'
                added_dot_ele = True
        # elif abs((query_sets.number - page_num) <= 1):#判断前后1页
        #     ele_class = ''
        #     if query_sets.number == page_num:
        #         added_dot_ele = False
        #         ele_class = "active"
        #     page_btns += '''<li class=%s><a href="?page=%s%s">%s</a></li>''' %(
        #     ele_class, page_num, filters, page_num)
        # else:#显示...
        #     if added_dot_ele == False:
        #         page_btns += '<li><a>...</a></li>'
        #         added_dot_ele = True
    return mark_safe(page_btns)






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
def render_filter_ele(filter_filed,admin_class,filter_conditions):
    # print(admin_class.model._meta.get_field(condtion))
    select_ele = "<select class='form-control' name='{filter_filed}'><option value=''>请选择</option>"
    field_obj = admin_class.model._meta.get_field(filter_filed)
    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            if filter_conditions.get(filter_filed) == str(choice_item[0]):
                selected = 'selected'
            select_ele+='''<option value='%s' %s>%s</option>''' % (choice_item[0],selected,choice_item[1])
            selected =''
    if  type(field_obj).__name__ == 'ForeignKey':
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_conditions.get(filter_filed) == str(choice_item[0]):
                selected = 'selected'
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0],selected,choice_item[1])
            selected = ''
    if type(field_obj).__name__ in ['DateField','DateTimeField']:
        date_els = []
        today_ele = datetime.now().date()
        date_els.append(['今天',datetime.now().date()])
        date_els.append(['昨天',today_ele - timedelta(days=1)])
        date_els.append(['近7天',today_ele - timedelta(days=7)])
        date_els.append(['本月',today_ele.replace(day=1)])
        date_els.append(['近30天',today_ele - timedelta(days=30)])
        date_els.append(['近90天',today_ele - timedelta(days=90)])
        date_els.append(['近180前',today_ele - timedelta(days=180)])
        date_els.append(['近365一年',today_ele - timedelta(days=365)])
        date_els.append(['年初',today_ele.replace(month=1,day=1)])
        selected = []
        for item in date_els:
            select_ele += '''<option value='%s' %s>%s</option>''' % (item[1], selected, item[0])
        filter_filed_name = "%s__gte" % filter_filed
    else:
        filter_filed_name = filter_filed
    select_ele += "</select>"
    select_ele = select_ele.format(filter_filed=filter_filed_name)
    return mark_safe(select_ele)

@register.simple_tag
def build_table_header_column(column,orderby_key,filter_conditions,admin_class):
    filters = ''
    for k, v in filter_conditions.items():
        filters += "&%s=%s" % (k, v)
    ele = '''<th><a href='?{filters}&o={orderby_key}'>{column}</a> \
          {sort_icon}</th>'''

    if orderby_key:
        if orderby_key.startswith('-'):
            sort_icon = "<span class='glyphicon glyphicon-chevron-up' aria-hidden='true'></span>"
        else:
            sort_icon = "<span class='glyphicon glyphicon-chevron-down' aria-hidden='true'></span>"
        if orderby_key.strip('-') == column:#排序的就是当前字段
            orderby_key=orderby_key

        else:
            sort_icon = ''
            orderby_key=column
    else:
        sort_icon = ''
        orderby_key = column
    try:
        column_verbose_name = admin_class.model._meta.get_field(column).verbose_name.upper()
    except FieldDoesNotExist as e:
        column_verbose_name = getattr(admin_class,column).display_name.upper()
        ele = '''<th><a href="javascript:void(0);">{column}</a></th>'''.format(column=column_verbose_name)
        return mark_safe(ele)
    ele = ele.format(filters=filters,orderby_key=orderby_key, column=column_verbose_name,sort_icon=sort_icon)
    return mark_safe(ele)


@register.simple_tag
def get_model_name(admin_class):
    model_name = admin_class.model._meta.verbose_name
    print(model_name)
    return model_name
@register.simple_tag
def get_m2m_obj_list(admin_class,field,form_obj):
    '''返回已选择的m2m数据'''
    #表结构对象的某个字段
    field_obj = getattr(admin_class.model,field.name)
    all_obj_list = field_obj.rel.field.related_model.objects.all()
    #单条数据的对象中的某个字段
    if form_obj.instance.id:
        obj_instance_field = getattr(form_obj.instance,field.name)
        selected_obj_list = obj_instance_field.all()
    else:
        return all_obj_list
    standly_obj_list = []
    for obj in all_obj_list:
        if obj not in selected_obj_list:
            standly_obj_list.append(obj)
    # print('======================================================= %s' % standly_obj_list)
    return standly_obj_list
@register.simple_tag
def print_obj_methods(obj):
    print('----------------debug %s----------------' % obj)
    print(dir(obj))

@register.simple_tag
def get_m2m_selected_obj_list(form_obj,field):
    '''返回已选择的m2m数据'''
    # print(form_obj.instance.id)
    if form_obj.instance.id:
        field_obj = getattr(form_obj.instance,field.name)
        return field_obj.all()

# @register.simple_tag
# def get_m2m_selected_obj_list(form_obj,field):
#     #if form_obj.instance.id:
#          field_obj = getattr(form_obj.instance,field.name)
#     return field_obj.all()