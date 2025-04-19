from django.contrib import admin
from django.urls import include, path
from oneplayerapp import views
# from rest_framework.routers import DefaultRouter
# from oneplayerapp.views import ClienteViewSet, AdministradorViewSet, ProductoViewSet
# router = DefaultRouter()
# router.register(r'clientes', ClienteViewSet)
# router.register(r'administradores', AdministradorViewSet)
# router.register(r'productos', ProductoViewSet)

urlpatterns = [

    # path('admin/', admin.site.urls),

    path('', views.oneplayer_view, name='inicio'),

    path('games/accion/', views.accion_view, name='accion'),

    path('games/carrera/', views.carrera_view, name='carrera'),

    path('games/FTP/', views.ftp_view, name='ftp'),

    path('games/MA/', views.ma_view, name='ma'),

    path('games/supervivencia/', views.supervivencia_view, name='supervivencia'),

    path('games/terror/', views.terror_view, name='terror'),

    path('auth/inicio_sesion/', views.inicio_sesion_view, name='inicio_sesion'),

    path('auth/form_registro/', views.registrarse_view, name='registrarse'),

    path('auth/registrar_org/', views.registrar_usuario_vw, name='registrarse_org'),

    path('user/cuenta/', views.cuenta_view, name='cuenta'),

    path('user/contraseña/', views.contraseña_view, name='contraseña'),

    path('user/carrito/', views.carrito_view, name='carrito'),

    path('user/gestion/', views.gestion_view, name='gestion'),

    path('auth/logout/', views.logout_view, name='logout'),

    path('checkout/', views.checkout_view, name='checkout'),

    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),

    # path('api/', include(router.urls)),
]
