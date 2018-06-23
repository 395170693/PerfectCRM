from django.db import models

# Create your models here.
class Customer(models.Model):
    '''客户跟进表'''
    pass

class CustomerFollowUp(models.Model):
    '''客户跟进表'''
    pass

class Course(models.Model):
    '''课程表'''
    pass

class ClassList(models.Model):
    '''班级表'''
    pass

class CourseRecord(models.Model):
    '''上课记录表'''
    pass

class Enrollment(models.Model):
    '''报名表'''
    pass

class UserProfile(models.Model):
    '''账号表'''
    pass

class Role(models.Model):
    '''角色表'''
    pass
