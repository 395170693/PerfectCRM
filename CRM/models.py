from django.db import models

# Create your models here.
class Customer(models.Model):
    '''客户跟进表'''
    name = models.CharField(max_length=32,blank=True,null=True)   #可以存取32个字节
    qq = models.CharField(max_length=64,unique=True)
    qq_name = models.CharField(max_length=64,blank=True,null=True)
    phone = models.CharField(max_length=64,blank=True,null=True)
    source_choices = (('0','转介绍'),
                      ('1', 'QQ群'),
                      ('2', '官网'),
                      ('3', '百度推广'),
                      ('4', '51CTO'),
                      ('5', '知乎'),
                      ('6', '市场推广'),
                    )
    source = models.SmallIntegerField(choices=source_choices)
    referral_from = models.CharField(verbose_name='转介绍人qq',max_length=64,blank=True,null=True)
    consult_course = models.ForeignKey("Course",verbose_name='咨询课程')
    content = models.TextField(verbose_name='咨询详情')
    tags = models.ManyToManyField('Tag',blank=True,null=True)
    consultant = models.ForeignKey('UserProfile')
    date = models.DateTimeField(auto_now_add=True)
    memo = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.qq
class Tag(models.Model):
    name = models.CharField(unique=True,max_length=32)

    def __str__(self):
        return self.name

class CustomerFollowUp(models.Model):
    '''客户跟进表'''
    customer = models.ForeignKey("Customer")
    content = models.TextField('跟进的内容')
    consultant = models.ForeignKey('UserProfile')
    intention_choices = (('0','2周内包名'),
                         (1, '1个月以内包名'),
                         (2, '近期无报名计划'),
                         (3, '在其他机构报名'),
                         (4, '已包名'),
                         (5, '已拉黑'),
                         )
    intention = models.SmallIntegerField(choices=intention_choices)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "<%s : %s>" % (self.customer.qq,self.intention)
class Course(models.Model):
    '''课程表'''
    name = models.CharField(max_length=64,unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name='周期(月)')
    outline = models.TextField()

    def __str__(self):
        return self.name
class Branch(models.Model):
    '''校区'''
    name = models.CharField(max_length=128,unique=True)
    addr = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class ClassList(models.Model):
    '''班级表'''
    branch = models.ForeignKey('Branch',verbose_name="校区")
    course = models.ForeignKey("Course")
    class_type_choices = ((0,'面授(脱产)'),
                          (1, '面授(周末)'),
                          (2, '网络班'),
                          )
    class_type = models.SmallIntegerField(choices=class_type_choices,verbose_name='班级类型')
    semester = models.PositiveSmallIntegerField(verbose_name='学期')
    teachers = models.ManyToManyField('UserProfile')



class CourseRecord(models.Model):
    '''上课记录表'''
    pass

class StudyRecord(models.Model):
    '''学习记录'''
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
