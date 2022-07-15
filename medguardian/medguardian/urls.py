"""medguardian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework import routers

import medications.views
import medications.forms
from .views import FrontPageView
from .views import RegistrationView
from .views import RegistrationSuccessView
from .views import LoginViewWrap
from .views import LogoutView
from .views import ProfileView
# from .views import ProfileViewSet


router = routers.DefaultRouter()
router.register('medications', medications.views.MedicationViewSet)
router.register('medication-products',
                medications.views.MedicationProductDetailsViewSet)
# router.register('accounts/profile', ProfileViewSet)
# router.register('medications/create', medications.forms.MedicationCreateForm)

print(router.urls)

urlpatterns = [
    path('', FrontPageView.as_view()),
    path('', include(router.urls)),
    path('register/', RegistrationView.as_view()),
    path('accounts/<int:pk>/profile/', ProfileView.as_view(), name='account_profile'),
    path('login', LoginViewWrap.as_view(), name='login'), # need this before 'accounts'
    path('logout/', LogoutView.as_view(), name='logout'),
    path('medication-search/', medications.views.medication_search),
    path('medications/create', medications.views.medication_create),
    path('account_created',
         RegistrationSuccessView.as_view(),
         name='account_created'),
    path('accounts/',
         include(('django.contrib.auth.urls', 'auth'), namespace='accounts')
         ),
    path('admin/', admin.site.urls),
]
