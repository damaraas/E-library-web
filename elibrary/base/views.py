import os
import pymupdf as fitz
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Buku, Profil
from django.conf import settings
from django.core.paginator import Paginator

@login_required
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Atur rute setelah login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def index(request):
    books = Buku.objects.all()

    is_favorite = request.GET.get('is_favorite')
    if is_favorite == "true":
        books = books.filter(is_favorite=True)
    else:
        books = Buku.objects.all()

    paginator = Paginator(books, 5)  # 5 buku per halaman

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj})

def toggle_favorite(request, book_id):
    book = get_object_or_404(Buku, id=book_id)
    book.is_favorite = not book.is_favorite  # Toggle status favorit
    book.save()
    return redirect(reverse('base:index'))

def profil(request):
    return render(request, 'profil.html')

def favorit(request):
    books = Buku.objects.filter(is_favorite=True)
    return render(request, 'favorit.html', {'books': books})

def authView(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("base:login")
    return render(request, "registration/register.html", {"form": form})

def upload(request):
    if request.method == "POST":
        judul = request.POST.get("judul")
        deskripsi = request.POST.get("deskripsi")
        penulis = request.POST.get("penulis")
        tahun = request.POST.get("tahun")
        genre = request.POST.get("genre")
        file_pdf = request.FILES.get("file_pdf")

        if file_pdf:
            fs = FileSystemStorage()
            pdf_filename = fs.save(f"pdfs/{file_pdf.name}", file_pdf)
            pdf_path = fs.path(pdf_filename)

            # Konversi PDF ke gambar
            pdf_document = fitz.open(pdf_path)
            image_paths = []

            for page_number in range(len(pdf_document)):
                page = pdf_document.load_page(page_number)
                pix = page.get_pixmap()
                img_filename = f"images/{file_pdf.name}_page_{page_number + 1}.png"
                img_path = os.path.join(settings.MEDIA_ROOT, img_filename)

                # Simpan gambar
                os.makedirs(os.path.dirname(img_path), exist_ok=True)
                pix.save(img_path)
                image_paths.append(f"media/{img_filename}")

            pdf_document.close()

            # Simpan ke database
            Buku.objects.create(
                judul=judul,
                deskripsi=deskripsi,
                penulis=penulis,
                tahun=tahun,
                genre=genre,
                file_pdf=pdf_filename,
                images=image_paths
            )

            return redirect("base:index")  # Redirect ke halaman katalog setelah berhasil upload

    return render(request, "upload.html")

def edit(request, book_id):
    book = get_object_or_404(Buku, id=book_id)

    if request.method == 'POST':
        # Ambil nilai dari form
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        penulis = request.POST.get('penulis')
        tahun = request.POST.get('tahun')

        if not judul:
            # Berikan pesan kesalahan jika judul kosong
            return render(request, 'edit.html', {
                'book': book,
                'error': 'Judul tidak boleh kosong.'
            })

        # Update data buku
        book.judul = judul
        book.deskripsi = deskripsi
        book.penulis = penulis
        book.tahun = tahun

        # Update file PDF jika ada
        file_pdf = request.FILES.get('file_pdf')
        if file_pdf:
            fs = FileSystemStorage()
            pdf_filename = fs.save(f"pdfs/{file_pdf.name}", file_pdf)
            book.file_pdf = pdf_filename

        book.save()
        return redirect('base:index')

    return render(request, 'edit.html', {'book': book})

def delete(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Buku, id=book_id)
    book.delete()

    return redirect('base:index')

def profil(request):
    # Ambil data profil dari database (misalnya, ambil satu profil pertama)
    profil = Profil.objects.first() 
    
    # Kirimkan data profil ke template
    return render(request, 'profil.html', {'profil': profil})

def edit_profil(request):
    user = get_object_or_404(Profil, email=request.user.email)

    if request.method == 'POST':
        nama = request.POST.get('first_name')
        email = request.POST.get('username')

        if not nama or not email:
            return render(request, 'edit_profil.html', {
                'user': user,
                'error': 'Nama dan email tidak boleh kosong.'
            })

        user.nama = nama
        user.email = email

        foto = request.FILES.get('foto')
        if foto:
            fs = FileSystemStorage()
            foto_filename = fs.save(f"fotoUser/{foto.name}", foto)
            user.foto = foto_filename

        user.save()
        return redirect('base:profil')

    return render(request, 'edit_profil.html', {'user': user})