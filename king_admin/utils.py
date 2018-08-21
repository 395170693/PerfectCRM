def table_filter(request,admin_class):
    '''进行条件过滤，并且返回过滤后的数据'''
    filter_conditions = {}
    for k,v in request.GET.items():
        if k == "page" or k == 'o':#保留的分页和排序关键字
            continue
        if v:
            filter_conditions[k] = v
    return admin_class.model.objects.filter(**filter_conditions),filter_conditions
def table_sort(request,admin_class,objs):
    orderby_key = request.GET.get('o')
    if orderby_key:
        return objs.order_by(orderby_key)
    return objs