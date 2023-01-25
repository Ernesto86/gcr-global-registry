from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from security.login import LogoutRedirectView, LoginAuthView
from security.main import MainView
from security.sign_up import SignUpView
from security.view.academic_level.view import AcademicLevelListView, AcademicLevelCreateView, AcademicLevelUpdateView, \
    AcademicLevelDeleteView
from security.view.directive.view import UserListView, UserCreateView, UserUpdateView, UserDeleteView
from security.view.organizador_detalle import OrganizadorRegistroListView
from security.view.organizador_registros import OrganizadorRegistrosView
from security.view.query_general import QueryGeneralView, CertificateStudentRegisterView, CertificateStudentSummaryView
from security.view.user import UserUpdatePasswordView
from security.forget_password import ResetPasswordView

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
    path('certificate-student-summary', CertificateStudentSummaryView.as_view(), name='certificate_student_summary'),
    path('organizador-registros', OrganizadorRegistrosView.as_view(), name='organizador-registros'),
    path('organizador-detalle/<int:typeregisterid>', OrganizadorRegistroListView.as_view(), name='organizador_detalle'),
    path('change-password', UserUpdatePasswordView.as_view(), name='user_change_password'),

    path('users', UserListView.as_view(), name='user_list'),
    path('users/create', UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>', UserDeleteView.as_view(), name='user_delete'),

    path('academic-levels', AcademicLevelListView.as_view(), name='academic_level_list'),
    path('academic-levels/create', AcademicLevelCreateView.as_view(), name='academic_level_create'),
    path('academic-levels/update/<int:pk>', AcademicLevelUpdateView.as_view(), name='academic_level_update'),
    path('academic-levels/delete/<int:pk>', AcademicLevelDeleteView.as_view(), name='academic_level_delete'),


    path('password-reset',ResetPasswordView.as_view(),name='password_reset'),
    #path('password-reset-confirm/<int:id>/<str:ced>/<str:token>/',solicitar_cambio_clave_form,name='solicitud_cambio_clave_form'),

]
