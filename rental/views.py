from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import (Amenities, rental, Reservation)
from django.db.models import Q



def check_booking(start_date  , end_date ,uid , room_count):
    qs = Reservation.objects.filter(
        start_date__lte=start_date,
        end_date__gte=end_date,
        hotel__uid = uid
        )
    
    if len(qs) >= room_count:
        return False
    
    return True
    
def rental(request):
    amenities_objs = Amenities.objects.all()
    rental_objs = rental.objects.all()

    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')
    print(amenities)
    if sort_by:
        if sort_by == 'ASC':
            rental_objs = rental_objs.order_by('rental_price')
        elif sort_by == 'DSC':
            rental_objs = rental_objs.order_by('-rental_price')

    if search:
        rental_objs = rental_objs.filter(
            Q(rental_name__icontains = search) |
            Q(description__icontains = search) )


    if len(amenities):
        rental_objs = rental_objs.filter(amenities__amenity_name__in = amenities).distinct()



    context = {'amenities_objs' : amenities_objs , 'rental_objs' : rental_objs , 'sort_by' : sort_by 
    , 'search' : search , 'amenities' : amenities}
    return render(request , 'rental.html' ,context)



def rental_detail(request,uid):
    hotel_obj = rental.objects.get(uid = uid)

    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout= request.POST.get('checkout')
        rental = rental.objects.get(uid = uid)
        if not check_booking(checkin ,checkout  , uid , rental.room_count):
            messages.warning(request, 'rental is already booked in these dates ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        Reservation.objects.create(rental=rental , user = request.user , start_date=checkin
        , end_date = checkout , Reservation_type  = 'Pre Paid')
        
        messages.success(request, 'Your booking has been saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

        
    
    return render(request , 'rental_detail.html' ,{
        'rental_obj' :rental_obj
    })

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.warning(request, 'Account not found ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(username = username , password = password)
        if not user_obj:
            messages.warning(request, 'Invalid password ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        login(request , user_obj)
        return redirect('/')

        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request ,'login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if user_obj.exists():
            messages.warning(request, 'Username already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create(username = username)
        user.set_password(password)
        user.save()
        return redirect('/')

    return render(request , 'register.html')
