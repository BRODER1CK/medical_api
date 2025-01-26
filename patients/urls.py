from django.urls import path
from .views import CustomTokenObtainPairView, PatientListCreateView, PatientRetrieveUpdateDeleteView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('patients/', PatientListCreateView.as_view(), name='patient_list_create'),
    path('patients/<int:pk>/', PatientRetrieveUpdateDeleteView.as_view(), name='patient_retrieve_update_delete'),
]