from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Recipe(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    recipe_name = models.CharField(max_length=50)
    recipe_info = models.TextField()
    image = models.ImageField(upload_to='images/app1')

    def __str__(self):
        return self.recipe_name