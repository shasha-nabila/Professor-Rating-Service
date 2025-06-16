from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProfessorViewSet, ModuleViewSet, RatingViewSet, RegisterView, LogoutView, ProfessorModuleAverageRatingView, RateProfessorView

def home_view(request):
    return JsonResponse({"message": "Welcome to the Professor Rating API"}, status=200)

router = DefaultRouter()
router.register(r'professors', ProfessorViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/average/<str:professor_id>/<str:module_code>/', ProfessorModuleAverageRatingView.as_view(), name='average'),
    path('api/rate/', RateProfessorView.as_view(), name='rate'),
]
