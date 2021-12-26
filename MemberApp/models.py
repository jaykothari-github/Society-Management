from django.db import models

# Create your models here.

class Member(models.Model):

    doc_choice = (
        ('Aadhar','Aadhar'),
        ('PAN','PAN'),
        ('DL','DL'),
        ('Other','Other'),
    )

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