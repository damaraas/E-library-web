from django.urls import path, include
from .views import authView, index, profil, favorit, toggle_favorite, login_view, upload, edit, delete, edit_profil
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", index, name="index"),
    path('login/', login_view, name='login'),
    path("register/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('profil/', profil, name='profil'),
    path('profil/edit', edit_profil, name='edit_profil'),
    path('favorites/', favorit, name='favorit'),
    path('toggle-favorite/<int:book_id>/', toggle_favorite, name='toggle_favorite'),
    path('upload/', upload, name='upload'),
    path('edit/<int:book_id>/', edit, name='edit'),
    path('delete/<int:book_id>/', delete, name='delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)