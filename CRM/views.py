from django.shortcuts import render
from CRM import forms,models
from django.db import IntegrityError


# Create your views here.
def index(request):
    return render(request,'sales/customers.html')

def customer_list(request):
    return render(request,'sales/customers.html')
#
# def stu_index(request):
#     return render(request,'stu_index.html')

def enrollment(request,customer_id):
    customer_obj = models.Customer.objects.get(id=customer_id)
    msgs = {}
    if request.method == "POST":
        enroll_form = forms.EnrollmentForm(request.POST)
        if enroll_form.is_valid():
            msg = "请将此链接发送给客户进行填写:http://127.0.0.1:8000/crm/customer/enrollment/{enroll_obj_id}/"
            # print("cleandata",enroll_form.cleaned_data)
            try:
                enroll_form.cleaned_data['customer'] = customer_obj
                enroll_obj = models.Enrollment.objects.create(**enroll_form.cleaned_data)
                msgs["msg"] = msg.format(enroll_obj_id=enroll_obj.id)
            except IntegrityError as e :
                enroll_obj = models.Enrollment.objects.get(customer_id = customer_obj.id,
                                                           enrolled_class_id=enroll_form.cleaned_data["enrolled_class"].id)
                msgs["msg"] = msg.format(enroll_obj_id=enroll_obj.id)
                enroll_form.add_error("__all__",'该用户的此条报名信息已经存在')
    else:
            enroll_form = forms.EnrollmentForm()
    return render(request,"sales/enrollment.html",{'enroll_form':enroll_form,'customer_obj':customer_obj,'msgs':msgs})