from django.db import models

class Members(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()



    image = models.ImageField(upload_to='members_pictures/')

    prediction = models.CharField(max_length=100)

    def __str__(self):
        return self.name