from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, RegisterUserView, LoginView

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversations")
router.register(r"messages", MessageViewSet, basename="messages")

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]

# Add router-generated URLs
urlpatterns += router.urls
