from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, informacion, servicios, obtener_regiones_comunas, mostrar_datos_formularios, lista_asesores, editar_asesor, eliminar_asesor, eliminar_formulario, registro
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('', index, name="index"),
    path('informacion/', informacion, name="informacion"),
    path('servicios/', servicios, name="servicios"),
    path('api/regiones-comunas/', obtener_regiones_comunas, name='obtener_regiones_comunas'),
    path('datos-formularios/', mostrar_datos_formularios, name='mostrar_datos_formularios'),
    path('asesores/', lista_asesores, name='lista_asesores'),
    path('asesores/editar/<int:asesor_id>/', editar_asesor, name='editar_asesor'),
    path('eliminar_asesor/<int:asesor_id>/', eliminar_asesor, name='eliminar_asesor'),
    path('eliminar_formulario/<int:formulario_id>/', eliminar_formulario, name='eliminar_formulario'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('registro/', registro, name='registro'),
]


    
