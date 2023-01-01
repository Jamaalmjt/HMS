from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('check_Reservation/' , check_Reservation),
    path('', rental , name='rental'),
    path('rental-detail/<uid>/' , rental_detail , name="rental_detail"),
    path('login/', login_page , name='login_page'),
    path('register/', register_page , name='register_page'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()
