from django.contrib import admin
from . models import Department, Position, Device, Personnel, CheckLogs, NCRI, office
#from .models import Views
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.admin.models import LogEntry
from zk import ZK, const

# Register your models here.
# @admin.register(Department)
# class DepartmentAdmin1(ImportExportModelAdmin):
#       pass
def clear_data(modeladmin, request, queryset):
    zk=ZK('192.168.8.100', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    conn = zk.connect()
    conn.clear_attendance()
    dev=Device()
    for i in queryset:
                    dev.id=i.id
                    dev.ip_address=i.ip_address
                    dev.mac_address=i.mac_address
                    dev.serial_number=i.serial_number
                    dev.user_count=i.user_count
                    dev.record_count='0'
                    dev.status="online"
                    dev.save()

def save_to_device(modeladmin, request, queryset):
    zk=ZK('192.168.8.100', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    conn = zk.connect()
    for q in queryset:
        print("Q",q.card_No)
        uid=q.id
        user_=str(q.id)
        print(type(user_))
        name=q.firstName+" "+q.lastName
        cardNO=q.card_No
        conn.set_user(uid, name=name, privilege='User', password='123', group_id='', user_id=str(uid), card=cardNO)
        #encode(user_,'utf-8')

        
        
        
        print(q.firstName)

        print(q.id)
admin.site.site_header = 'VILLA SOMALIA'                    # default: "Django Administration"
admin.site.index_title = 'ID CHECKING APP'                 # default: "Site administration"
admin.site.site_title = 'ID Checking Application'

class DepartmentAdmin(ImportExportModelAdmin):
    search_fields=['deptName']
    list_display=('id','deptName')
    actions=[save_to_device,]
    pass
class officeAdmin(admin.ModelAdmin):
    list_display=('id','office_name')
    search_fields=['office_name']
    pass
class NCRI_RESOURCE(resources.ModelResource):
    class Meta:
        model=NCRI
        #exclude=('id',)
class NCRI_Admin(ImportExportModelAdmin):
    resource_class=NCRI_RESOURCE
    search_fields=['fistName']

    list_per_page=30
    list_display=(
        'id',
        'personnelNo',
        'fistName',
        'department',
        'date',
        'weekday',
        'exception',
        'check_in_time',
        'check_out_time',
        'total_time',
        'late',
        'early_leave',
        'absent'
    )
    pass


   

class AttendanceLogAdmin(ImportExportModelAdmin):
    search_fields=['personnel','date']
    list_display=('id','personnel','date','time')

class DeviceAdmin(admin.ModelAdmin):
     list_display=(
        'mac_address',
        'ip_address',
        'serial_number',
       # 'card_count',
        'user_count',
        'record_count',
        'status',
     )
     actions=[clear_data]

class PersonnelAdmin(ImportExportModelAdmin):

   
    #model=Personnel

    search_fields=['firstName']
    list_display=(
        'id',
        'firstName',
        'lastName',
        'age',
        'mobile',
        'card_No',
        'office',

        #'image',
        'deptment',
        'position',
        'date'
    )
    actions=[save_to_device, ]

    pass
class PositionAdmin(ImportExportModelAdmin):
    search_fields=['titleName']
    list_display=('id','titleName','date')

   
    class Meta:
     model=Position
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(CheckLogs,  AttendanceLogAdmin)
# admin.site.register(NCRI, NCRI_Admin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(office, officeAdmin)
admin.site.register(LogEntry)



