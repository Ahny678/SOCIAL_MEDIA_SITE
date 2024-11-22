from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='def.jpg', upload_to='profile_pics')
    name = models.CharField(max_length=255)
    bio = models.TextField()
    followers = models.ManyToManyField(User, blank=True, related_name='followers')

    def __str__(self):
        return f"{self.user.username}'s Profile" 

    #to resize the image
    def save(self,*args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if this.image == 'def.jpg':
                pass
            elif this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super(Profile,self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
