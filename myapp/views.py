from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from myapp.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,logout, login
# Create your views here.

def index(request):
    return render(request, 'index.html')

def login_user(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user1 = authenticate(username=username, password=password)
        if user1 is not None:
            login(request ,user1)
            return redirect('/train_list')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request ,'login_user.html')
    return render(request ,'login_user.html')

def register_user(request):
    if request.method =='POST':
        Uname = request.POST.get('Uname')
        email= request.POST.get('email')
        password= request.POST.get('password')
        confirm_password= request.POST.get('confirm_password')
        phone_no=request.POST.get('phone_no')
        address=request.POST.get('address')

        if password==confirm_password:
            if User.objects.filter(username=Uname).exists() or User.objects.filter(email=email).exists():
                messages.error(request,"Username or email already taken")
                return redirect('/register_user')
            else:
                #my db user
                user1 = UserInfo(Uname=Uname, email=email , password=password ,phone_no=phone_no ,address=address)
                user1.save()

                #official django user
                user=User.objects.create_user(username=Uname, email=email , password=password)
                user.save()
                messages.success(request, "Profile details updated.")
                return redirect('/login_user')
        else:
            messages.error(request,"INVALID PASSWORDS")
            return redirect('/register_user')
    return render(request,'register_user.html')

def logout_user(request):
    logout(request)
    return redirect('/login_user')

#actual pages

#enter what the user wants to do and display valid trains
def train_list(request):

    if request.user.is_anonymous:
        return redirect('/login_user')
    
    if request.method =='POST':
        source = request.POST.get('source')
        destination= request.POST.get('destination')
        Sclass = request.POST.get('Sclass')
        no_of_seats = int (request.POST.get('no_of_seats'))
        date = request.POST.get('date')

        #in ticket simply retrive the latest object
        date1= hold_date(date=date)
        date1.save()

        matching_trains = Train.objects.filter(
        source=source,
        destination=destination).filter(
        seat__seat_class=Sclass,
        seat__available_seats__gte=no_of_seats
        ).distinct().order_by('seat__cost_per_seat')


        train_data = []
        for train in matching_trains:
            seats = Seat.objects.filter(Train_no=train, seat_class=Sclass, available_seats__gte=no_of_seats)
            for seat in seats:
                total_cost = seat.cost_per_seat * no_of_seats
                train_data.append({
                    'train': train,
                    'source':source,
                    'destination':destination,
                    'no_of_seats':no_of_seats,
                    'seat_class': seat.seat_class,
                    'available_seats': seat.available_seats,
                    'cost_per_seat': seat.cost_per_seat,
                    'total_cost': total_cost,
                })

        context = {
            'train_data': train_data,
        }
        print(context)
        
        #MAYBE SOME ERROR IN REDIRECTING
        return render(request, 'book_train.html', context)
    
    
    return render(request,'train_list.html')

def book_train(request, train_id, seat_class, no_of_seats):
    train = get_object_or_404(Train, id=train_id)
    seat = get_object_or_404(Seat, Train_no=train, seat_class=seat_class)

    # Ensure the train has enough available seats
    #uid = request.user //enjoi
    # Create a new ticket
    '''
    Ticket1 = Ticket.objects.create(
    Ticket_no=Ticket.objects.count() + 1, 
    Status='Confirmed',
    Train_no=train,
    #UID=uid, //enjoi # Assuming Uname is just a placeholder for a user field
    )
    '''

    Ticket1 = Ticket(Ticket_no=Ticket.objects.count() + 1, Status='Confirmed',Train_no=train,#UID=uid, //enjoi # Assuming Uname is just a placeholder for a user field
    )
    Ticket1.save()

    seat.available_seats -= no_of_seats
    seat.save()
    context={'ticket_id':Ticket1.id}
    #return render(request,'validate_credit_card.html',context)
    return redirect(f'/validate_credit_card/{Ticket1.id}')

        


def checkLuhn(cardNo):
     
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False
     
    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')
     
        if (isSecond == True):
            d = d * 2
        nSum += d // 10
        nSum += d % 10
  
        isSecond = not isSecond
     
    if (nSum % 10 == 0):
        return True
    else:
        return False
 
def validate_credit_card(request,ticket_id):
    print(ticket_id)
    if request.method == "POST":
        card_number = request.POST.get('card_number')
        #card_holder=request.POST.get('card_holder')
        #expiry_date=request.POST.get('expiry_date')
        #CVV =request.POST.get('cvv')
        
        if card_number and card_number.isdigit() and checkLuhn(card_number):
            return redirect(f'/booking_confirmation/{ticket_id}')

        else:
            messages.error(request,"Invalid Credit Card Number")
            return redirect(f'/validate_credit_card/{ticket_id}')    
        
        #context={'ticket_id':ticket_id}
        #return redirect(f'/booking_confirmation/{ticket_id}')
        #return render(request,'booking_confirmation.html',context)     
    

    return render(request, 'validate_credit_card.html')

#return ticket data
def booking_confirmation(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    print(ticket)
    #ticket = get_object_or_404(Ticket, Ticket_no=ticket_id)
    latest_date = hold_date.objects.latest('date')
    print(latest_date)
    return render(request, 'booking_confirmation.html', {'ticket': ticket, 'date': latest_date })