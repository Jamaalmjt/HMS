from django.contrib.auth.models import User
from django.db import models
import uuid

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Amenities(BaseModel):
    amenity_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.amenity_name

class rental(BaseModel):
    rental_name= models.CharField(max_length=100)
    rental_price = models.IntegerField()
    description = models.TextField()
    amenities = models.ManyToManyField(Amenities)
    room_count = models.IntegerField(default=10)

    def __str__(self) -> str:
        return self.hotel_name


class rentalImages(BaseModel):
    rental= models.ForeignKey(rental ,related_name="images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to="rental")



class Reservation(BaseModel):
    rental_name= models.ForeignKey(rental  , related_name="Reservation" , on_delete=models.CASCADE)
    Reservation_id= models.ForeignKey(User, related_name="Reservation_id" , on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    Reservation_type= models.CharField(max_length=100,choices=(('Pre Paid' , 'Pre Paid') , ('Post Paid' , 'Post Paid')))

def confirm(request, pk = None):
    if request.method == 'POST':
        if pk:
             rental_name = rental.objects.get(pk = pk)
             guest_id = request.user
             check_in = request.session['check_in'] 
             check_out = request.session['check_out']
             reservation = Reservation(
             check_in = check_in, 
             check_out = check_out,
             rental_id = rental_id.id,
             guest_id = guest_id.id
             )
             reservation.save()

             book_in = datetime.strptime(check_in, '%Y-%m-%d').date()
             book_out = datetime.strptime(check_out, '%Y-%m-%d').date()
             reserved = False

             delta = timedelta(days = 1)
             while book_in <= book_out:
                  rental_id.reserved = True
                  book_in += delta
             else:
                  rental_id.reserved = False

      return render(request, "system/reserve.html", args)
