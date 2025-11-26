from django.db import models

class Foto(models.Model):
    titulo = models.CharField(max_length=100)
    # 'upload_to' crea una subcarpeta dentro de 'media'
    imagen = models.ImageField(upload_to='fotos/') 

    def __str__(self):
        return self.titulo