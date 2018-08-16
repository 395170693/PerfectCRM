def table_filter(request,admin_class):
    '''进行条件过滤，并且返回过滤后的数据'''
    filter_conditions = {}
    for k,v in request.GET.items():
        if v:
            filter_conditions[k] = v
    return admin_class.model.objects.filter(**filter_conditions),filter_conditions

