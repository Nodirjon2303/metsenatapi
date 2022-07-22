from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'university', UniversityApiView)
router.register(r'student', StudentApiView)
router.register(r'homiy', HomiyApiView)
router.register(r'ariza', ArizaApiView)
