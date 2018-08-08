from django import template
register=template.Library()
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