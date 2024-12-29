from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
import time
from datetime import date
from django.db.models import Avg, Sum, Min, Max
from owner.models import *
import datetime
# Create your views here
def daly_report(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        shope = Shope.objects.filter(mobile=mobile).first()
        
        d = ((datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))

        item = []
        for i in Item.objects.filter(shope_id=shope.id, status=1).order_by('name'):
            opening = Purchase.objects.filter(item_id=i.id, shope_id=shope.id,date__lte=d).aggregate(Sum('qty'))['qty__sum']
            if opening==None:
                opening = 0
            sales = Sales.objects.filter(item_id=i.id, shope_id=shope.id,date__lte=d).aggregate(Sum('qty'))['qty__sum']
            if sales:
                opening -= int(sales)
                
                
            closing = opening
            if closing == None:
                closing = 0
            s = Sales.objects.filter(item_id=i.id, shope_id=shope.id,date=date.today()).aggregate(Sum('qty'))['qty__sum']
            if s:
                closing -= int(s)
            
            if s == None:
                s=0
            purchase = Purchase.objects.filter(item_id=i.id, shope_id=shope.id,date=date.today()).aggregate(Sum('qty'))['qty__sum']
            if purchase:
                closing += purchase
            else:
                purchase = 0
            item.append({'name':i.name,'opn':opening,'clo':closing, 'sales':s, 'purchase':purchase})


        context={
            'shope':shope,
            'date':date.today(),
            'item':item
        }
        return render(request, 'pdf/daly_report.html', context)
    else:
        return redirect('login')