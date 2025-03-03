# E-Library

## Deskripsi
Proyek **e-Library** adalah sebuah aplikasi berbasis web yang dikembangkan menggunakan **Django** untuk mengelola koleksi buku dalam format PDF. Aplikasi ini memungkinkan pengguna untuk mengunggah, mengedit, menghapus, serta menandai buku sebagai favorit. Selain itu, pengguna juga memiliki profil yang dapat diperbarui.

## Teknologi yang Digunakan
- **Backend**: Django 5.x
- **Database**: SQLite (default Django database)
- **Frontend**: HTML, CSS, Tailwind CSS, JavaScript
- **File Handling**: Django FileSystemStorage
- **PDF Processing**: PyMuPDF (pymupdf)
- **Authentication**: Django Authentication

## Instalasi dan Menjalankan Proyek
### 1. Clone Repository
```sh
https://github.com/damaraas/elibrary.git
```

### 2. Masuk Virtual Environment
```sh
source .venv/bin/activate  # Untuk Mac/Linux
.venv\Scripts\activate    # Untuk Windows
```

### 3. Install Dependensi
```sh
pip install -r requirements.txt
```

### 4. Masuk Folder elibrary
```sh
pip install -r requirements.txt
```

### 5. Jalankan Migrasi Database
```sh
python manage.py makemigrations
python manage.py migrate
```

### 6. Buat Superuser (Opsional)
```sh
python manage.py createsuperuser
```
atau dapat login menggunakan:  
Email: damarasalsabila@gmail.com  
Password: damsal123

### 7. Jalankan Server
```sh
python manage.py runserver
```

### 8. Jalankan Tailwind di terminal berbeda
```sh
python manage.py tailwind start
```

Akses aplikasi di **http://127.0.0.1:8000/**

## Catatan Penting
- Semua file PDF yang diunggah akan disimpan di dalam folder `media/pdfs/`.
- Gambar hasil konversi dari PDF akan disimpan di dalam `media/images/`.
- Pastikan folder `media/` memiliki izin baca/tulis agar file dapat disimpan.
