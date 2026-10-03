from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address= models.CharField(max_length=3000)
    gender= models.CharField(max_length=30)

class detect_fraud_in_banking(models.Model):

    CID= models.CharField(max_length=3000)
    CName= models.CharField(max_length=3000)
    Gen= models.CharField(max_length=3000)
    Age= models.CharField(max_length=3000)
    State= models.CharField(max_length=3000)
    City= models.CharField(max_length=3000)
    BB= models.CharField(max_length=3000)
    AT= models.CharField(max_length=3000)
    TID= models.CharField(max_length=3000)
    TDate= models.CharField(max_length=3000)
    TTime= models.CharField(max_length=3000)
    TAmount= models.CharField(max_length=3000)
    MID= models.CharField(max_length=3000)
    TType= models.CharField(max_length=3000)
    MCat= models.CharField(max_length=3000)
    ABal= models.CharField(max_length=3000)
    TDevice= models.CharField(max_length=3000)
    TLoc= models.CharField(max_length=3000)
    TCur= models.CharField(max_length=3000)
    TDesc= models.CharField(max_length=3000)
    Prediction= models.CharField(max_length=3000)

class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



