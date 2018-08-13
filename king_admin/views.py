from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import importlib


# Create your views here.
from king_admin import king_admin

def index(request):
    return render(request,'king_admin/table_index.html',{'table_list':king_admin.enabled_admins})

def display_table_objs(request,app_name,table_name):
    print ('-------------->',app_name,table_name)
    admin_class = king_admin.enabled_admins[app_name][table_name]
    # models_module = importlib.import_module('%s.model'%(app_name))
    # model_obj = getattr(models_module,table_name)
    object_list = admin_class.model.objects.all()
    paginator = Paginator(object_list, 2) # Show 25 contacts per page

    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    #return render(request, 'list.html', {'contacts': contacts})
    #admin_class = king_admin.enabled_admins[app_name][table_name]
    return render(request,'king_admin/table_objs.html',{"query_sets":query_sets})
