from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from security.login import logout_user, LoginAuthView
from security.main import MainView
from security.view.organizador_detalle import OrganizadorRegistroListView
from security.view.organizador_registros import OrganizadorRegistrosView
from security.view.query_general import QueryGeneralView

urlpatterns = [
    path(
        'token/create/',
        jwt_views.TokenObtainPairView.as_view(),
        name='token-create'
    ),
    path(
        'token/refresh/',
        jwt_views.TokenRefreshView.as_view(),
        name='token-refresh'
    ),
    # path('token/auth', CustomTokenObtainPairView.as_view(), name='token-auth'),
    # modulo de seguridad frontend
    path('login', LoginAuthView.as_view(), name='login'),
    path('logout', logout_user),
    path('main', MainView.as_view(), name='main'),
    path('query-general', QueryGeneralView.as_view(), name='query_general'),
    path('organizador-registros', OrganizadorRegistrosView.as_view(), name='organizador-registros'),
    path('organizador-detalle/<int:typeregisterid>', OrganizadorRegistroListView.as_view(), name='organizador_detalle'),
]
