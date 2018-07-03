from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def customer_list(request):
    return render(request,'customers.html')

def stu_index(request):
    return render(request,'stu_index.html')