from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    '''客户'''
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
    status_choices = ((0, '已报名'), (1, '未报名'), (2, '已退学'))
    status = models.SmallIntegerField(choices=status_choices)
    date = models.DateTimeField(auto_now_add=True)
    memo = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.qq
    class Meta:
        verbose_name = "客户"
        verbose_name_plural = "客户"




class Tag(models.Model):
    name = models.CharField(unique=True,max_length=32)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"




class CustomerFollowUp(models.Model):
    '''客户跟进表'''
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
    content = models.TextField('跟进的内容')
    status_choices = (
        (0,'绝无报名计划'),
        (1,'一个月内报名'),
        (2,'2周内报名'),
        (3,'已报名其它机构'),
    )
    status = models.SmallIntegerField(choices=status_choices)



    consultant = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
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
    class Meta:
        verbose_name = "客户跟进"
        verbose_name_plural = "客户跟进"




class Course(models.Model):
    '''课程表'''
    name = models.CharField(max_length=64,unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name='周期(月)')
    outline = models.TextField()
    class Meta:
        verbose_name = "课程"
        verbose_name_plural = "课程"


    def __str__(self):
        return self.name
class Branch(models.Model):
    '''校区'''
    name = models.CharField(max_length=128,unique=True)
    addr = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "校区"
        verbose_name_plural = "校区"


class ClassList(models.Model):
    '''班级表'''
    branch = models.ForeignKey('Branch',verbose_name="校区",on_delete=models.CASCADE)
    course = models.ForeignKey("Course",on_delete=models.CASCADE)
    class_type_choices = ((0,'面授(脱产)'),
                          (1, '面授(周末)'),
                          (2, '网络班'),
                          )
    class_type = models.SmallIntegerField(choices=class_type_choices,verbose_name='班级类型')
    semester = models.PositiveSmallIntegerField(verbose_name='学期')
    teachers = models.ManyToManyField('UserProfile')
    start_date = models.DateField(verbose_name='开班日期')
    end_date = models.DateField(verbose_name='截止日期',blank=True,null=True)
    def __str__(self):
        return "%s  %s  %s" %(self.branch,self.course,self.semester)
    class Meta:
        unique_together = ('branch','course','semester')
        verbose_name = "班级"
        verbose_name_plural = "班级"

class CourseRecord(models.Model):
    '''上课记录表'''
    from_class = models.ForeignKey('ClassList',verbose_name='班级',on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name='第几节（天）')
    teacher = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=12,blank=True,null=True)
    homework_content = models.TextField(blank=True,null=True)
    outline = models.TextField("本节课程的大纲")
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return "%s %s" % (self.from_class,self.day_num)

    class Meta:
        unique_together = ("from_class","day_num")
        verbose_name = "上课记录"
        verbose_name_plural = "上课记录"
class StudyRecord(models.Model):
    '''学习记录'''
    student = models.ForeignKey("Enrollment",on_delete=models.CASCADE)
    course_record = models.ForeignKey('CourseRecord',on_delete=models.CASCADE)
    attendance_choice = ((0,'已签到'),
                         (1, '迟到'),
                         (2, '缺勤'),
                         (3, '早退'),
                                )
    attendance = models.SmallIntegerField(choices=attendance_choice,default=0)

    score_choices = ((100,"A+"),
                     (90, "A"),
                     (85, "B+"),
                     (80, "B"),
                     (75, "B-+"),
                     (70, "C+"),
                     (60, "C"),
                     (40, "C-"),
                     (-50, "D"),
                     (-100, "COPY"),
                     (0, "N/A"),
                     )
    score = models.SmallIntegerField(choices=attendance_choice)
    memo = models.TextField(blank=True,null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return "%s %s %s" % (self.student,self.course_record,self.score)
    class Meta:
        unique_together = ('student','course_record')
        verbose_name = "学习记录"
        verbose_name_plural = "学习记录"
class Enrollment(models.Model):
    '''报名表'''
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey("ClassList",verbose_name="所报班级",on_delete=models.CASCADE)
    consultanr = models.ForeignKey("UserProfile",verbose_name="课程顾问",on_delete=models.CASCADE)
    contract_agreed = models.BooleanField(default=False,verbose_name="学员已同意合同条款")
    contract_approved = models.BooleanField(default=False,verbose_name="合同已经审核")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.customer,self.enrolled_class)
    class Meta:
        unique_together = ("customer","enrolled_class")
        verbose_name = "报名"
        verbose_name_plural = "报名"
class Payment(models.Model):
    "付款表"
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
    course = models.ForeignKey("Course",verbose_name="所报课程",on_delete=models.CASCADE)
    amount  = models.PositiveIntegerField(verbose_name="数额",default=500)
    consultant = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s %s' % (self.customer,self.amount)
    class Meta:
        verbose_name = "缴费记录"
        verbose_name_plural = "缴费记录"

class UserProfile(models.Model):
    '''账号表'''
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField("Role",blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        #verbose_name = "账号表"
        verbose_name_plural = "账号"
class Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=32,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "角色"
        verbose_name_plural = "角色"