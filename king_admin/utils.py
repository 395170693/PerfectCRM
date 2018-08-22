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
    print(orderby_key)
    if orderby_key:
        res = objs.order_by(orderby_key)
        if orderby_key.startswith('-'):
            orderby_key = orderby_key.strip('-')
        else:
            orderby_key = '-%s' % orderby_key
    else:
        res = objs
    return res,orderby_key

def table_seach(request,admin_class,object_list):
