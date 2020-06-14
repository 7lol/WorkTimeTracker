from rest_framework import routers
from WorkLog import views

router = routers.DefaultRouter()
router.register(r'positions', views.PositionViewSet, basename="home")