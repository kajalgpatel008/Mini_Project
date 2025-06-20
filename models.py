from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.PositiveIntegerField()
    remarks = models.TextField()

    def __str__(self):
        return self. name

class User(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.PositiveIntegerField()
    address = models.TextField()
    password = models.CharField(max_length=100)
    user_image=models.ImageField(upload_to='user_images/',default='user_images/default.png')

    def __str__(self):
        return self.fname+' '+ self.lname 