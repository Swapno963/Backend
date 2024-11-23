from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    id = models.AutoField(primary_key=True)
    menu_id = models.PositiveIntegerField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        # Set menu_id to id + 500 when the object is first created
        if not self.menu_id:
            super(Menu, self).save(*args, **kwargs)  
            self.menu_id = self.id + 500  
            self.save(update_fields=['menu_id'])  

        else:
            super(Menu, self).save(*args, **kwargs)  # Save the object normally if menu_id already exists

    def __str__(self):
        return self.name
