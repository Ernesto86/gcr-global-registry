from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from security.login import logout_user, LoginAuthView

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
]
