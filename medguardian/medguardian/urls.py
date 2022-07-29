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
from prescriptions.views import PrescriberCreateView
from prescriptions.views import PrescriberSelectView
from prescriptions.views import PrescriptionCreateView
from prescriptions.views import PrescribersListView
from prescriptions.views import PrescriberAddSuccessView
from prescriptions.views import PrescriptionRDView
from prescriptions.views import AdministrationTimeListView
from prescriptions.views import PrescriptionUpdateAPIView
from prescriptions.views import TodaysMedicationsListView
from prescriptions.views import download_todays_meds



# med_router = medications.views.MedicationRouter(trailing_slash=False)
# med_router.register(prefix='medications',
#                     viewset=medications.views.ActiveMedProfileViewSet,
#                     basename='medications'
#                    )

router = routers.DefaultRouter()
# router.register(r'medications',
#                 medications.views.ActiveMedProfileViewSet,
#                 basename='medications'
#                )
# router.register('medications', medications.views.MedicationViewSet)
router.register('medication-products',
                medications.views.MedicationProductDetailsViewSet)
# router.register('accounts/profile', ProfileViewSet)
# router.register('medications/create', medications.forms.MedicationCreateForm)

urlpatterns = [
    path('', FrontPageView.as_view()),
    path('register/', RegistrationView.as_view(), name='register'),
    path('account_created',
         RegistrationSuccessView.as_view(),
         name='account_created'),
    path('login', LoginViewWrap.as_view(), name='login'),  # need this before 'accounts'
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/<int:pk>/profile/', ProfileView.as_view(), name='account_profile'),
    path('accounts/<int:pk>/prescriptions/new', PrescriptionCreateView.as_view(), name='new_rx'),
    path('accounts/<int:pk>/prescriptions/<int:rx_id>', PrescriptionRDView.as_view(), name='prescription'),
    path('account/<int:pk>/prescriptions/<int:rx_id>/administration_times',
         AdministrationTimeListView.as_view(),
         name='admin_times'),
    path('accounts/<int:pk>/prescribers/new', PrescriberCreateView.as_view(), name='new_prescriber'),
    path('accounts/<int:pk>/prescribers/select', PrescriberSelectView.as_view(), name='select_prescriber'),
    path('accounts/<int:pk>/prescribers', PrescribersListView.as_view(), name='prescribers'),
    path('account/<int:pk>/prescriber/<int:prescriber_id>/added',
         PrescriberAddSuccessView.as_view(),
         name='prescriber_add_success'),
    path('accounts/<int:pk>/medications', medications.views.ActiveMedProfileViewSet.as_view(), name='medications'),
    path('accounts/<int:pk>/prescriptions/today', TodaysMedicationsListView.as_view(), name='todays_meds'),
    path('accounts/<int:pk>/prescriptions/today/download', download_todays_meds, name='todays_meds_download'),
    path('accounts/<int:pk>/prescriptions/<int:rx_id>/administration_times/edit',
         PrescriptionUpdateAPIView.as_view(),
         name='edit_admin_times'),
    path('medication-search/', medications.views.medication_search),
    path('medications/create', medications.views.medication_create),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='accounts')),
    path('admin/', admin.site.urls),
]
