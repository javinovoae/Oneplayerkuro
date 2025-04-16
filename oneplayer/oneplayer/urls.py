from django.contrib import admin
from django.urls import path
from oneplayerapp import views


urlpatterns = [

    #path('admin/', admin.site.urls),

    # Página principal
    path('', views.oneplayer_view, name='inicio'),

    # Categorías
    path('games/accion/', views.accion_view, name='accion'),
    path('games/carrera/', views.carrera_view, name='carrera'),
    path('games/FTP/', views.ftp_view, name='ftp'),
    path('games/MA/', views.ma_view, name='ma'),
    path('games/supervivencia/', views.supervivencia_view, name='supervivencia'),
    path('games/terror/', views.terror_view, name='terror'),

    # Autenticación
    path('auth/inicio_sesion/', views.inicio_sesion_view, name='inicio_sesion'),
    path('auth/form_registro/', views.registrarse_view, name='registrarse'),

    # Usuarios (clientes y admin)
    path('user/cuenta/', views.cuenta_view, name='cuenta'),
    path('user/contraseña/', views.contraseña_view, name='contraseña'),

    # Solo clientes
    path('user/carrito/', views.carrito_view, name='carrito'),

    # Panel administrador
    path('user/gestion/', views.gestion_view, name='gestion'),

    # Logout
    path('auth/logout/', views.logout_view, name='logout'),

]
