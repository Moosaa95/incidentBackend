from django.urls import path

from app.views import (IncidentListCreateView, IncidentRetrieveUpdateDestroyView,
                        LocationListCreateView, LocationRetrieveUpdateDestroyView, 
                        UserRegistrationAPIView,UserLoginAPIView, 
                        CustomTokenObtainPairView, ReportListCreateView,
                          ReportDetailView, DashboardAPIView,
                          CustomUserListCreateView, UserProfileEditView,
                          ChangePasswordView, GetUserDetailByEmailView
                    )

urlpatterns = [
    # Other URL patterns
    path('create-user/', UserRegistrationAPIView.as_view(), name='create-user'),
    path('get-users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('locations/<int:pk>/', LocationRetrieveUpdateDestroyView.as_view(), name='location-retrieve-update-destroy'),
    path('incidents/', IncidentListCreateView.as_view(), name='incident-list-create'),
    path('incidents/<int:pk>/', IncidentRetrieveUpdateDestroyView.as_view(), name='incident-retrieve-update-destroy'),
    path('reports/', ReportListCreateView.as_view(), name='report-list-create'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
    path('edit-profile/', UserProfileEditView.as_view(), name='edit-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('get-user-detail/', GetUserDetailByEmailView.as_view(), name='get-user-name-by-email'),

]