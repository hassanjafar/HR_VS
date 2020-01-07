from django.shortcuts import render
from . models import Department, Personnel, Position, Device, CheckLogs, NCRI
from django.core import serializers
from django.http import JsonResponse, HttpResponse, Http404, FileResponse
from django.forms.models import model_to_dict
from ast import literal_eval
import json
from django.core.serializers.json import DjangoJSONEncoder
from zk import ZK, const
from django.db.models import Count, Sum, Q, F, When, Case, Value, ExpressionWrapper, FloatField, IntegerField
from django.db.models.functions import Coalesce, Extract
import datetime
from django.contrib.auth.decorators import login_required
from django.db import connection

from datetime import datetime


# Create your views here.
#ncri report quer
def logout (request):
    return render (request, 'accounts/login.html')

@login_required(login_url='/accounts/login')
def test(request):
    userlog=request.user
    context={"user":userlog}
    return render(request, 'idapp/test.html', context)

@login_required(login_url='/accounts/login')
def dashboard(request):
    return render(request, 'idapp/dashboard.html')
def dash_report(request):
    count=0
    att_sliced=[]
    q=Device.objects.values()
    var=0
    for i in q:
        var=i['id']
    try:
        zk=ZK('192.168.8.100', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        print(zk)
        dev=Device()
        conn = zk.connect()
        
        if zk.is_connect:
        #    print("we are inside")
            
        #   print(zk.get_users())
            
            
            if var > 0:
                print("if near online block", var)
                conn.get_users()
                conn.get_attendance()
                dev.id=var
                dev.ip_address=str(zk._ZK__address)
                dev.mac_address=str(zk.get_mac())
                dev.serial_number=str(zk.get_serialnumber())
                dev.user_count=str(conn.users)
                dev.record_count=str(conn.records)
                
                dev.status="online"
                dev.save()
            else:
                print("else near online block")
                conn.get_users()
                conn.get_attendance()
                dev.ip_address=str(zk._ZK__address)
                dev.mac_address=str(zk.get_mac())
                dev.serial_number=str(zk.get_serialnumber())
                dev.user_count=str(conn.users)
                dev.record_count=str(conn.records)
                dev.status="online"
                dev.save()
                print(zk)
        
            

        att=conn.get_attendance()
        last=CheckLogs.objects.values('date').last()
        obj=CheckLogs()
        if last:
            #print("we are in last")
            last_val=last['date']
            print("last value =",last, type(last))
            

            
            
            for i in att:
                        count=count+1
                        att_val=i.timestamp.date()
                        if last_val==att_val:
                            att_sliced=att[count:]
                            break
            if count!=0:
                        print("reaching if count!=0")
                        for a in att_sliced:
                            #print("true a ==", a.user_id)
                            date_val= a.timestamp.date()
                            time_val=a.timestamp.time()
                            check_val=CheckLogs.objects.values().filter(date=date_val, time=time_val)
                        # print(check_val.count())
                            if check_val.count()==0:
                                u_id=a.user_id
                                #print("u_id=",u_id)
                                check_user=Personnel.objects.filter(id=u_id)
                                print(check_user)
                                if check_user.count()!=0:
                                    #print(time_val,"we can insert straightly")
                                    obj.personnel=Personnel(a.user_id)
                                    obj.date=date_val
                                    obj.time=time_val
                                    obj.save()
            elif att:
                for i in att:
                    per=i.user_id
                    check_user=Personnel.objects.filter(id=per)
                    print(check_user)
                    if check_user.count()!=0:
                            date_val= i.timestamp.date()
                            
                            obj.personnel=Personnel(per) 
                            time_val=i.timestamp.time()
                            obj.date= date_val
                            obj.time=time_val
                                
                            obj.save()       
    # except:  double check validity of this condition
            if var < 0:
                print("not reached here")
          
                for i in q:
                    dev.id=i['id']
                    dev.ip_address=i['ip_address']
                    dev.mac_address=i['mac_address']
                    dev.serial_number=i['serial_number']
                    dev.user_count=i['user_count']
                    dev.record_count=i['user_count']
                    dev.status="offline"
                    dev.save()
                    
                
            
            
        else:
            att=conn.get_attendance()
            for i in att:
                obj.time=i.timestamp.time()
                obj.date=i.timestamp.date()
                obj.personnel=Personnel(i.user_id)
                obj.save()
        # print("we are here")
    except:
        if zk.is_connect==False:
            for i in q:
                    dev.id=i['id']
                    dev.ip_address=i['ip_address']
                    dev.mac_address=i['mac_address']
                    dev.serial_number=i['serial_number']
                    dev.user_count=i['user_count']
                    dev.record_count=i['user_count']
                    dev.status="offline"
                    dev.save()
        print("network error")
    
    
    date_sel=datetime.today().date()
    vip= Personnel.objects.filter(deptment_id__deptName='VIP').count()
    que=CheckLogs.objects.filter(date=date_sel).count()
    staff=Personnel.objects.values().count()
    query_res=CheckLogs.objects.count()
    
  
    
    context={'query':query_res, 'vip':vip, 'staff':staff, 'que':que}
    return JsonResponse (context, safe=False)
    

def gatetwo(request):


    #algo note
    # connect to device 
    #read last id in list pass it to the query id to select
    # return and then display
    # second option live_pro

          ######################
    # for attendance in conn.live_capture():
    # if attendance is None:
    #     # implement here timeout logic
    #     pass
    # else:
    data=dict()
    val=''
    no=0
    zk=ZK('192.168.8.100', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    conn = zk.connect()

    att=conn.get_attendance()
    #print("lists displayed  ==",att[38:])
    for att in conn.live_capture():
        if att is None:
             print("not found")
             no=-1
             break
        else:
            print("found",att.user_id)
            no=att.user_id
            break

    
   
    users=conn.get_users()
    ##print(users[1].name)
    query_res= Personnel.objects.filter(id=no).values('id','firstName','lastName','image',
    'deptment__deptName','ID_CARD','office__office_name','date', 'position__titleName')

    query=json.dumps(list(query_res), cls=DjangoJSONEncoder)



    
    #data['val']=literal_eval(query)

    print(query)
    context={'query':query}
    return JsonResponse (context, safe=False)










def report(request):
    from_date=request.GET['_date']
    end_date=request.GET['date2']

    query_res=NCRI.objects.filter(~Q(weekday='Friday'), date__lte=end_date, date__gte=from_date).\
     values('personnelNo','fistName','department').order_by('fistName').\
     annotate(saacadaha= Coalesce(Extract(Sum('total_time'), 'hours' ), Value(0)), \
         tar=Count('date'), absent=Coalesce(Sum('absent'),Value(0)),\
     fasax=Count('exception',filter=Q(exception__contains='Holi')),\
    #  check=Sum('check_in_time'),\
      
     sick=Count('exception',filter=Q(exception__contains='Sick')),
     annual=Count('exception', filter=Q(exception__contains='Annual')), \
     maalmaha_shaqa_kujira_bishan=ExpressionWrapper(F('tar')-F('absent')-F('fasax')-F('sick')-F('annual'),
     output_field=FloatField()), saacadaha_shaqada=ExpressionWrapper(F('tar')*8, output_field=FloatField()),\
     maamlmaha_dhiman=ExpressionWrapper(F('tar')-F('maalmaha_shaqa_kujira_bishan'),output_field=FloatField()), \
    saacaadaha_dhiman=ExpressionWrapper(F('saacadaha_shaqada')-F('saacadaha'),output_field=IntegerField())
         )

    # with connection.cursor() as cursor:
        
         
    # testquery=NCRI.objects.raw ('SELECT "ID_App_ncri"."personnelNo", "ID_App_ncri"."fistName", "ID_App_ncri"."department", COALESCE(SUM("ID_App_ncri"."total_time"), 0) AS "saacadaha", COUNT("ID_App_ncri"."date") AS "tar", COALESCE(SUM("ID_App_ncri"."absent"), 0) AS "absent", COUNT("ID_App_ncri"."exception") FILTER (WHERE "ID_App_ncri"."exception" LIKE "%Holi%") AS "fasax", COUNT("ID_App_ncri"."exception") FILTER (WHERE "ID_App_ncri"."exception" LIKE "%Sick%") AS "sick", COUNT("ID_App_ncri"."exception") FILTER (WHERE "ID_App_ncri"."exception" LIKE "%Annual%") AS "annual", ((((COUNT("ID_App_ncri"."date") - COALESCE(SUM("ID_App_ncri"."absent"), 0)) - COUNT("ID_App_ncri"."exception") FILTER (WHERE "ID_App_ncri"."exception" LIKE "%Holi%")) - COUNT("ID_App_ncri"."exception") FILTER (WHERE "ID_App_ncri"."exception" LIKE "%Sick%")) - COUNT("ID_App_ncri"."exception") FILTER (WHERE "ID_App_ncri"."exception" LIKE "%Annual%")) AS "maalmaha_shaqa_kujira_bishan", (COUNT("ID_App_ncri"."date") * 8) AS "saacadaha_shaqada", (COUNT("ID_App_ncri"."date") - ((((COUNT("ID_App_ncri"."date") - COALESCE(SUM("ID_App_ncri"."absent"), 0)) - COUNT("ID_App_ncri"."exception") FILTER (WHERE "ID_App_ncri"."exception" LIKE "%Holi%")) - COUNT("ID_App_ncri"."exception") FILTER (WHERE "ID_App_ncri"."exception" LIKE "%Sick%")) - COUNT("ID_App_ncri"."exception") FILTER (WHERE "ID_App_ncri"."exception" LIKE "%Annual%"))) AS "maamlmaha_dhiman", ((COUNT("ID_App_ncri"."date") * 8) - COALESCE(SUM("ID_App_ncri"."total_time"), 0)) AS "saacaadaha_dhiman" FROM "ID_App_ncri" WHERE (NOT ("ID_App_ncri"."weekday" = "Friday") AND "ID_App_ncri"."date"  between "2019-10-01" AND "2019-10-31" GROUP BY "ID_App_ncri"."personnelNo", "ID_App_ncri"."fistName", "ID_App_ncri"."department" ORDER BY "ID_App_ncri"."fistName" ASC')   
    # print("====",testquery)
    # for test in testquery:
    #      print(test)
   # query = serializers.serialize('json', query_res, fields= ('personnelNo','fistName','department'))
    query=json.dumps(list(query_res), cls=DjangoJSONEncoder)
    
    #print(query)
    #print("_date ==",request.GET['_date'])
    context={'query':query}
    return JsonResponse(context, safe=False)

@login_required(login_url='/accounts/login')

def reports(request):
    userlog=request.user
    context={"user":userlog}
    return render(request, 'idapp/ncrireport.html',context)


def callapi(request):
    print(request)

    return render(request,'idapp/gatetwo.html')

def gatetwohorizantal(request):
    return render(request, 'idapp/gatetwohorizantal.html')
    
@login_required(login_url='/accounts/login')

def login (request):
    return render (request, 'idapp/dashboard.html')

@login_required(login_url='/accounts/login')
def pdf_generate(request):
    from_date=request.GET['_date']
    end_date=request.GET['date2']
    print(end_date)
    pdf=PDF()
    pdf.add_page('L')
    

    query_res=NCRI.objects.filter(~Q(weekday='Friday'), date__lte=end_date, date__gte=from_date, department='Logistic Department').\
     values('personnelNo','fistName','department').order_by('fistName').\
     annotate(saacadaha= Coalesce(Extract(Sum('total_time'), 'hours' ), Value(0)), \
         tar=Count('date'), absent=Coalesce(Sum('absent'),Value(0)),\
     fasax=Count('exception',filter=Q(exception__contains='Holi')),\
    #  check=Sum('check_in_time'),\
      
     sick=Count('exception',filter=Q(exception__contains='Sick')),
     annual=Count('exception', filter=Q(exception__contains='Annual')), \
     maalmaha_shaqa_kujira_bishan=ExpressionWrapper(F('tar')-F('absent')-F('fasax')-F('sick')-F('annual'),
     output_field=FloatField()), saacadaha_shaqada=ExpressionWrapper(F('tar')*8, output_field=FloatField()),\
     maamlmaha_dhiman=ExpressionWrapper(F('tar')-F('maalmaha_shaqa_kujira_bishan'),output_field=FloatField()), \
    saacaadaha_dhiman=ExpressionWrapper(F('saacadaha_shaqada')-F('saacadaha'),output_field=IntegerField())
         )
    #date_time=datetime.today() 
#  Employee.objects.all().filter(SHRD_NO='NCR-100').values('SHRD_NO','NCRI_NO','FULL_NAME','NICK_NAME','DATE_OF_BIRTH',\
#        'PLACE','SEX','PHOTO','NEIGHBORHOOD','DISTRICT','REGION','MOBILE1',\
#          'EMAIL1','MOBILE2','EMAIL2','TITLE_id__title','DEPARTMENT_id__department',\
#          'SECTION_id__section','SUPERVISOR','WORKPLACE','GRADE_id__grade','SALARY_FGS','SALARY_UNHCR',\
#          'TAX','NET','DATE_OF_EMPL','REF_NAME','REF_MOBILE','Shift_id__Type_OF_Shift','document__document')
    #  total query



    

    date_time=datetime.strptime(from_date,'%Y-%m-%d')
       
    pdf.body(query_res, date_time)
    pdf.output('ncri111.pdf','F')

  
    query=json.dumps(list(query_res), cls=DjangoJSONEncoder)
    
   # print(query)
    
    context={'query':query}
    return JsonResponse(context, safe=False)


@login_required(login_url='/accounts/login')
def pdf_response(request):
    #  _date=request.GET['_date']
    #  print(_date)
     try:
        return FileResponse(open('ncri111.pdf', 'rb'), content_type='application/pdf')
     except FileNotFoundError:
        raise Http404()

