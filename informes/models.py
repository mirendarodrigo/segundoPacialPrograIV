from django.db import models

class Reporte(models.Model):
    nombre = models.CharField(max_length=100)
    contenido = models.TextField(help_text="Texto que saldrá en el PDF")
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre