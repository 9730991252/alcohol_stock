from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import *
from owner.models import *
from datetime import date
from django.db.models import Avg, Sum, Min, Max
import datetime
# Create your views here.

def search_item (request):
    if request.method == 'GET':
        item_name = request.GET['item_name']
        shope_id = request.GET['shope_id']
        item = ''
        if item_name:
            item = Item.objects.filter(name__icontains=item_name,shope_id=shope_id)
        context={
            'item':item,
            'p':Purchase.objects.filter(shope_id=shope_id).last()
        }
        t = render_to_string('ajax/search_item.html',context)
    return JsonResponse({'t': t})

def search_item_sales (request):
    if request.method == 'GET':
        item_name = request.GET['item_name']
        shope_id = request.GET['shope_id']
        item = []
        d = ((datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
        if item_name:
            for i in Item.objects.filter(name__icontains=item_name,shope_id=shope_id):
                stock = Purchase.objects.filter(item_id=i.id, shope_id=shope_id,date__lte=d).aggregate(Sum('qty'))['qty__sum']
                if stock==None:
                    stock = 0
                    
                s = Sales.objects.filter(item_id=i.id, shope_id=shope_id).aggregate(Sum('qty'))['qty__sum']
                if s:
                    stock -= int(s)
                    
                item.append({'name':i.name,'id':i.id,'stock':stock})
                
        context={
            'item':item,
            'p':Purchase.objects.filter(shope_id=shope_id).last()
        }
        t = render_to_string('ajax/search_item_sales.html',context)
    return JsonResponse({'t': t})
        
