from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Customize how the token is parsed or validated here
        return super().authenticate(request)
