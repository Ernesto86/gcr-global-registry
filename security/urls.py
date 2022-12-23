from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from security.login import LogoutRedirectView, LoginAuthView
from security.main import MainView
from security.sign_up import SignUpView
from security.view.organizador_detalle import OrganizadorRegistroListView
from security.view.organizador_registros import OrganizadorRegistrosView
from security.view.query_general import QueryGeneralView, CertificateStudentRegisterView
from security.view.user import UserUpdatePasswordView

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
    path('sign-up', SignUpView.as_view(), name='sign_up'),
    path('logout', LogoutRedirectView.as_view(), name='logout'),
    path('main', MainView.as_view(), name='main'),
    path('query-general', QueryGeneralView.as_view(), name='query_general'),
    path('certificate-student-register', CertificateStudentRegisterView.as_view(), name='certificate_student_register'),
    path('organizador-registros', OrganizadorRegistrosView.as_view(), name='organizador-registros'),
    path('organizador-detalle/<int:typeregisterid>', OrganizadorRegistroListView.as_view(), name='organizador_detalle'),
    path('change-password', UserUpdatePasswordView.as_view(), name='user_change_password'),
]
