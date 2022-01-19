from django.db import models
# from MemberApp.models import Member

# Create your models here.

class SecUser(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    pic = models.FileField(upload_to='Profile',default='avatar.png')
    setting = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Emergency(models.Model):

    cate_choice = (
        ('Doctor','Doctor'),
        ('Plumber','Plumber'),
        ('Electrician','Electrician'),
        ('Cate','Cate'),
    )

    uid = models.ForeignKey(SecUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=13)
    email = models.EmailField()
    occupation = models.CharField(max_length=50,choices=cate_choice)
    des = models.TextField()

    def __str__(self):
        return self.name + '   ' + self.occupation 


class Gallery(models.Model):

    uid = models.ForeignKey(SecUser,on_delete=models.CASCADE)
    pic = models.FileField(upload_to='Gallery')

    def __str__(self):
        return self.uid.name + ' >  ' + str(self.pic.url)