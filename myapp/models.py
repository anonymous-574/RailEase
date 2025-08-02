from django.db import models

# Create your models here.


#use 2 seperate tables
#user is django default , authenthicate there
#then save Data in USER AND USER_INFO

class UserInfo(models.Model):
    Uname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=50)
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.Uname


class Train(models.Model):
    Train_no = models.IntegerField() 
    Tname = models.CharField(max_length=50)
    Atime = models.CharField(max_length=50)
    Dtime = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)

    def __str__(self):
        return self.Tname +' '+ self.source + ' '+ self.destination
    
class Seat(models.Model):
    Train_no = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat_class = models.CharField(max_length=50)  
    available_seats = models.IntegerField()
    cost_per_seat = models.IntegerField()

    def __str__(self):
        return str(self.id) +' '+ self.seat_class


class Ticket(models.Model):
    Ticket_no=models.IntegerField()
    Status= models.CharField(max_length=50)
    Train_no = models.ForeignKey(Train, on_delete=models.CASCADE)
    #UID= models.ForeignKey(user_info, on_delete=models.CASCADE) //enjoi


class hold_date(models.Model):
    date = models.DateField()