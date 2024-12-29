from django.shortcuts import render, redirect
from sunil.models import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
import math
from datetime import date
from django.db.models import Avg, Sum, Min, Max
# Create your views here.
def owner_home(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        shope = Shope.objects.filter(mobile=mobile).first()
        item_stock = []
        for i in Item.objects.filter(shope_id=shope.id):
            stock = Purchase.objects.filter(item_id=i.id, shope_id=shope.id).aggregate(Sum('qty'))['qty__sum']
            if stock==None:
                stock = 0
            s = Sales.objects.filter(item_id=i.id, shope_id=shope.id).aggregate(Sum('qty'))['qty__sum']
            if s:
                stock -= int(s)
            item_stock.append({'name':i.name,'id':i.id,'stock':stock})
        context={
            'shope':shope,
            'item_stock':item_stock
        }
        return render(request, 'owner/owner_home.html', context)
    else:
        return redirect('login')
    
def report(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        shope = Shope.objects.filter(mobile=mobile).first()
        context={
            'shope':shope
        }
        return render(request, 'owner/report.html', context)
    else:
        return redirect('login')
    
    
@csrf_exempt
def sales(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        shope = Shope.objects.filter(mobile=mobile).first()
        if shope:
            if 'Sales'in request.POST:
                qty = request.POST.get('qty')
                item_id = request.POST.get('item_id')
                Sales(
                    shope_id=shope.id,
                    item_id=item_id,
                    qty=qty,
                ).save()
                return redirect('sales')
        context={
            'shope':shope,
            'sales':Sales.objects.filter(shope_id=shope.id,date=date.today())
            
        }
        return render(request, 'owner/sales.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def purchase(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        shope = Shope.objects.filter(mobile=mobile).first()
        if 'Purchase'in request.POST:
            qty = request.POST.get('qty')
            purchase_invoice_number = request.POST.get('purchase_invoice_number')
            item_id = request.POST.get('item_id')
            Purchase(
                shope_id=shope.id,
                item_id=item_id,
                qty=qty,
                purchase_invoice_number=purchase_invoice_number
            ).save()
            return redirect('purchase')
        context={
            'shope':shope,
            'purchase':Purchase.objects.filter(shope_id=shope.id,date=date.today())
        }
        return render(request, 'owner/purchase.html', context)
    else:
        return redirect('login')

def item(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        shope = Shope.objects.filter(mobile=mobile).first()
        if 'Add_item'in request.POST:
            name = request.POST.get('name').upper()
            if Item.objects.filter(name=name,shope_id=shope.id).exists():
                pass
            else:
                Item(
                    shope_id=shope.id,
                    name=name,
                ).save()
            return redirect('item')
        if 'Edit_item'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name').upper()
            if Item.objects.filter(name=name,shope_id=shope.id).exclude(id=id).exists():
                pass
            else:
                Item(
                    id=id,
                    shope_id=shope.id,
                    name=name,
                ).save()
            return redirect('item')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = Item.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect('item')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Item.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect('item')
        context={
            'shope':shope,
            'item':Item.objects.filter(shope_id=shope.id)
        }
        return render(request, 'owner/item.html', context)
    else:
        return redirect('login')