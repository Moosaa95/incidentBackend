# from rest_framework import generics
# from .models import CustomUser
# from .serializers import CustomUserSerializer

# class CreateUserView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import get_user_model
from .dashboard import Dashboard

from .models import Incident, Location, Report, CustomUser
from .serializers import CustomTokenObtainPairSerializer, CustomUserSerializer, IncidentSerializer, LocationSerializer, UserLoginSerializer, ReportSerializer
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.views import TokenObtainPairView

class UserRegistrationAPIView(APIView):
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        print('before login')
        serializer = self.serializer_class(data=request.data)
        print('serializer', serializer)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Authenticate the user
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Login the user
                login(request, user)
                user_info = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                print('hey loser get out of here')
                return Response({'message': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class IncidentListCreateView(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    # def perform_create(self, serializer):
    #     # Set the reporter field to the currently authenticated user
    #     print(serializer, 'jerhefbkj')
        # serializer.save(reporter=self.request.user)

class IncidentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer


class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class DashboardAPIView(APIView):
    def get(self, request):
        dashboard = Dashboard()  # Create an instance of your Dashboard class
        total_users = dashboard.get_total_users()
        total_reports = dashboard.get_total_reports()
        total_incidents = dashboard.get_total_incidents()
        pending_incidents = dashboard.get_pending_incidents()
        resolved_incidents = dashboard.get_resolved_incidents()

        data = {
            "total_users": total_users,
            "total_reports": total_reports,
            "total_incidents": total_incidents,
            "pending_incidents": pending_incidents,
            "resolved_incidents": resolved_incidents,
        }

        return Response(data)


class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer