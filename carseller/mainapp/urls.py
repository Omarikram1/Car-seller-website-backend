from django.urls import path

from mainapp.API.CRUDCars import CarCrudApi
from . import views
from .controllers.UserController import SignupView,activate,LoginView,sendemail,landingpage
from .API.SearchApi import FilterCarsApi
from .Pages.ViewFunctions import home
from .API.GetFrontPageInfo import GetType
#SignupOtp,resend_otp

urlpatterns = [
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('home',home.as_view(),name='home'),
    path('login/',LoginView,name='login'),
    path('emailsent',sendemail,name='emailsent'),
    path('',landingpage,name='landingpage'),
    path('home/specifiedcars/',FilterCarsApi.as_view(),name='TypeFilter'),
    path('GetType/',GetType.as_view(),name='GetType'),
    path('managecars/',CarCrudApi.as_view(),name='ManageCars')



    # path('home/specifiedcarspage',specifiedcarsview.as_view(),name= 'specifiedcarspage')
    # path('resend_otp', resend_otp, name='resend_otp'),
    # path('resend_otp/', resend_otp, name='resend_otp'),
    # path('signup_otp_verification',SignupOtp.as_view(),name='signup_otp_verification'),
]

