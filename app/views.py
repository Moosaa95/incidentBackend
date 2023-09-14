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
from django.contrib.auth import update_session_auth_hash
from .models import Incident, Location, Report, CustomUser
from .serializers import CustomTokenObtainPairSerializer, CustomUserSerializer, IncidentSerializer, LocationSerializer, UserLoginSerializer, ReportSerializer, UserProfileEditSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
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


class UserProfileEditView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileEditSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# class ChangePasswordView(generics.UpdateAPIView):
#     serializer_class = ChangePasswordSerializer
#     model = CustomUser
#     # permission_classes = [IsAuthenticated]

#     def get_object(self, queryset=None):
#         return self.request.user

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)
#         print(serializer, 'serial')

#         if serializer.is_valid():
#             old_password = serializer.data.get("old_password")
#             new_password = serializer.data.get("new_password")
            
#             # Check the old password
#             if not self.object.check_password(old_password):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
#             # Change the password
#             self.object.set_password(new_password)
#             self.object.save()
#             update_session_auth_hash(request, self.object)  # Important for maintaining the user's session
            
#             return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            
            # Check the old password
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Change the password
            self.object.set_password(new_password)
            self.object.save()
            update_session_auth_hash(request, self.object)  # Important for maintaining the user's session
            
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserDetailByEmailView(APIView):
    def get(self, request):
        # Get the email from the query parameters
        email = request.query_params.get('user_id')
        print(email, 'email id')

        if not email:
            return Response({'error': 'Email is required as a query parameter.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try to find a user with the provided email
            user = CustomUser.objects.get(id=email)
            print(user, 'before')
            serializer = CustomUserSerializer(user)  # Serialize the user data
            print('after', serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found for the provided email.'}, status=status.HTTP_404_NOT_FOUND)