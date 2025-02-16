from django.db import models

class Buku(models.Model):
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField()
    penulis = models.CharField(max_length=255)
    tahun = models.IntegerField()
    genre = models.CharField(max_length=100)
    file_pdf = models.FileField(upload_to="pdfs/")
    images = models.JSONField(default=list)  # Menyimpan path hasil konversi PDF ke gambar
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.judul

class Profil(models.Model):
    nama = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    foto = models.FileField(upload_to="fotoUser/")

    def __str__(self):
        return self.nama