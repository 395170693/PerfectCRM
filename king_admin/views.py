from django.shortcuts import render,redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import importlib
from king_admin.utils import table_filter,table_sort,table_seach
from king_admin.forms import create_model_form


# Create your views here.
from king_admin import king_admin

def index(request):
    return render(request,'king_admin/table_index.html',{'table_list':king_admin.enabled_admins})

def display_table_objs(request,app_name,table_name):
    #print ('-------------->',app_name,table_name)
    admin_class = king_admin.enabled_admins[app_name][table_name]

        # models_module = importlib.import_module('%s.model'%(app_name))
        # model_obj = getattr(models_module,table_name)
        #object_list = admin_class.model.objects.all()
    object_list,filter_conditions = table_filter(request,admin_class) #过滤都得结果
    object_list = table_seach(request,admin_class,object_list)
    object_list,orderby_key = table_sort(request,admin_class,object_list) #排序后的结果

    paginator = Paginator(object_list, admin_class.list_per_page) # Show 25 contacts per pag
    # def get_page(self, number):
    #     """
    #     Return a valid page, even if the page argument isn't a number or isn't
    #     in range.
    #     """
    #     try:
    #         number = self.validate_number(number)
    #     except PageNotAnInteger:
    #         number = 1
    #     except EmptyPage:
    #         number = self.num_pages
    #     return self.page(number)

    page = request.GET.get('page')
    query_sets = paginator.get_page(page)
    # try:
    #     query_sets = paginator.get_page(page)
    # except PageNotAnInteger:
    #     query_sets = paginator.get_page(1)
    # except EmptyPage:
    #     query_sets = paginator.get_page(paginator.num_pages)

    #return render(request, 'list.html', {'contacts': contacts})
    admin_class = king_admin.enabled_admins[app_name][table_name]
    return render(request,'king_admin/table_objs.html',{"admin_class":admin_class,
                                                        "query_sets":query_sets,
                                                        'filter_conditions':filter_conditions,
                                                        'orderby_key':orderby_key,
                                                        'previous_orderby':request.GET.get('o') or '',
                                                        "search_text":request.GET.get('_q','')
                                                        })
def table_objs_change(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)

    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == 'POST':
        form_obj = model_form_class(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
    else:
        # obj = admin_class.model.objects.get(id=obj_id)
        form_obj = model_form_class(instance=obj)
    print('22222222222222222222222222222222222222222222')
    print(type(form_obj))
    print(form_obj)

    return render(request,'king_admin/table_obj_change.html',{'form_obj':form_obj,'admin_class':admin_class})

def table_objs_add(request,app_name,table_name):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)

    if request.method == 'POST':#新增
        form_obj = model_form_class(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(request.path.replace('/add','/'))
    else:
        # obj = admin_class.model.objects.get(id=obj_id)
        form_obj = model_form_class()
    return render(request,'king_admin/table_obj_add.html',{'form_obj':form_obj})