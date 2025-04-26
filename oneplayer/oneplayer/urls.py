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
    path('auth/registrar_org/', views.registrar_usuario_vw, name='registrarse_org'),
    path('auth/registro/', views.registrarse_view, name='registro'),
    path('auth/logout/', views.logout_view, name='logout'),

    path('user/cuenta/', views.cuenta_view, name='cuenta'),
    path('user/cambiar_contraseña/', views.editar_contraseña_org, name='cambiar_contraseña'),
    path('user/contraseña/', views.cambiar_contraseña_view, name='contraseña'),
    path('user/carrito/', views.carrito_view, name='carrito'),
    path('user/gestion/', views.gestion_view, name='gestion'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('editar_perfil/', views.editar_perfil_org, name='editar_perfil'),


    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('carrito/finalizar/', views.finalizar_compra, name='finalizar_compra'),

    path('categorias/', views.gestionar_categorias, name='gestion_categorias'),
    path('categorias/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('user/agregar_juego/', views.agregar_juego, name='agregar_juego'),

    # path('api/', include(router.urls)),
]
