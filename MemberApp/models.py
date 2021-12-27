from django.db import models

from SecApp.models import SecUser

# Create your models here.

class Member(models.Model):

    doc_choice = (
        ('Aadhar','Aadhar'),
        ('PAN','PAN'),
        ('DL','DL'),
        ('Other','Other'),
    )

    uid = models.ForeignKey(SecUser,on_delete=models.CASCADE,null=True)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    doc = models.CharField(max_length=30,choices=doc_choice)
    doc_number = models.CharField(max_length=20)
    flat_no = models.CharField(max_length=10)
    address = models.TextField()
    password = models.CharField(max_length=20)
    pic = models.FileField(upload_to='member',default='avatar.png')
    verify = models.BooleanField(default=False)


    def __str__(self):
        return self.fname + '  ' + self.fname + ' ->  ' + str(self.flat_no)


class Event(models.Model):

    uid = models.ForeignKey(SecUser,on_delete=models.CASCADE)
    event_name = models.CharField(max_length=90)
    event_des = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    event_at = models.DateField()
    pic = models.FileField(upload_to='Event',null=True,blank=True)
    interest = models.ManyToManyField(Member,related_name='Likes')

    def __str__(self):
        return self.event_name + '  @  ' + str(self.event_at)