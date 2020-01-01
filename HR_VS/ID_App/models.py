from django.db import models

from django.utils.timezone import now
#from django.db.models import UniqueConstraint

# Create your models here.


class Department(models.Model):
    deptName=models.CharField(max_length=200)
    
    def __str__(self):
        return self.deptName

class Position(models.Model):
    titleName=models.CharField(max_length=200)
    date=models.DateTimeField(default=now)
    def __str__(self):
        return self.titleName

class office(models.Model):
    office_name=models.CharField(max_length=200)
    def __str__(self):
       return self.office_name
class Personnel (models.Model):
    firstName=models.CharField(max_length=200)
    lastName=models.CharField(max_length=200)
    ID_CARD=models.CharField(max_length=200)
    age=models.IntegerField()
    mobile=models.IntegerField()
    card_No=models.CharField(max_length=200)
    image=models.ImageField(upload_to='images/media', default='images/media/no-image.png')
    deptment=models.ForeignKey(Department, on_delete=models.CASCADE)
    position=models.ForeignKey(Position, on_delete=models.CASCADE)
    office=models.ForeignKey(office, on_delete=models.CASCADE, null=True, blank=True)
    date=models.DateField(default=now)
    def __str__(self):
        return self.firstName+' '+self.lastName

class CheckLogs(models.Model):
    personnel=models.ForeignKey(Personnel, on_delete=models.CASCADE)
    date=models.DateField(default=now)
    time=models.TimeField()
    
    class Meta:
       constraints=[ models.UniqueConstraint(fields=['personnel','date','time'], name='unique_att_log1')]
    # def __str__(self):
    #     return self.personnel__fistName

class Device(models.Model):
    mac_address=models.CharField(max_length=200)
    ip_address=models.CharField(max_length=200)
    serial_number=models.CharField(max_length=200)
   # card_count=models.CharField(max_length=200)
    user_count=models.CharField(max_length=200)
    record_count=models.CharField(max_length=200)
    status=models.CharField(max_length=200, default='offline')
class NCRI(models.Model):
    personnelNo=models.CharField(max_length=200, null=True)
    fistName=models.CharField(max_length=200)
    department=models.CharField(max_length=200)
    date=models.DateField(default=now)
    weekday=models.CharField(max_length=200)
    exception=models.CharField(max_length=200, null=True)
    check_in_time=models.TimeField(null=True)
    check_out_time=models.TimeField(null=True)
    total_time=models.TimeField(null=True)
    
    late=models.TimeField(null=True)
    early_leave=models.TimeField(null=True)
    absent=models.IntegerField(null=True)
    class Meta:
        constraints=[ models.UniqueConstraint(fields=[
            # 'personnelNo',
            'fistName',
            # 'department',
            'date',
            # 'weekday',
            # 'exception',
            # 'check_in_time',
            # 'check_out_time',
            # 'total_time',
            # 'late',
            # 'early_leave',
            # 'absent'
        ], 
        name='unique_ncri_log')]
    




    

    
