from .models import  Report, Incident, CustomUser
from django.contrib.auth import get_user_model



User = get_user_model()

class Dashboard:
    def __init__(self):
        pass

    def get_total_users(self):
        # Replace this with your logic to fetch the total number of users from your data source (e.g., database).
        return CustomUser.objects.count()  # Assuming you're using Django ORM.

    def get_total_reports(self):
        # Replace this with your logic to fetch the total number of reports from your data source.
        return Report.objects.count()

    def get_total_incidents(self):
        # Replace this with your logic to fetch the total number of incidents from your data source.
        return Incident.objects.count()

    def get_pending_incidents(self):
        # Replace this with your logic to fetch the count of pending incidents from your data source.
        return Incident.objects.filter(status='pending').count()

    def get_resolved_incidents(self):
        # Replace this with your logic to fetch the count of resolved incidents from your data source.
        return Incident.objects.filter(status='resolved').count()

# Example usage:
# dashboard = Dashboard()
# total_users = dashboard.get_total_users()
# total_reports = dashboard.get_total_reports()
# total_incidents = dashboard.get_total_incidents()
# pending_incidents = dashboard.get_pending_incidents()
# resolved_incidents = dashboard.get_resolved_incidents()

# print(f"Total Users: {total_users}")
# print(f"Total Reports: {total_reports}")
# print(f"Total Incidents: {total_incidents}")
# print(f"Pending Incidents: {pending_incidents}")
# print(f"Resolved Incidents: {resolved_incidents}")
