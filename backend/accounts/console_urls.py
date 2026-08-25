from django.urls import path

from .console_api import (
    DepartmentListView,
    DepartmentDetailView,
    EmployeeListView,
    EmployeeResetPasswordView,
    EmployeeRoleView,
    LdapSettingsView,
    LdapTestConnectionView,
    LoginAttemptLogListView,
    SecuritySettingsView,
)

urlpatterns = [
    # Departments
    path("departments/", DepartmentListView.as_view(), name="console-departments"),
    path("departments/<int:pk>/", DepartmentDetailView.as_view(), name="console-department-detail"),
    
    # Employees
    path("employees/", EmployeeListView.as_view(), name="console-employees"),
    path("employees/<int:pk>/reset-password/", EmployeeResetPasswordView.as_view(), name="console-employee-reset-password"),
    path("employees/<int:pk>/role/", EmployeeRoleView.as_view(), name="console-employee-role"),
    
    # LDAP
    path("ldap-settings/", LdapSettingsView.as_view(), name="console-ldap-settings"),
    path("ldap-settings/test/", LdapTestConnectionView.as_view(), name="console-ldap-settings-test"),
    
    # Security
    path("security-settings/", SecuritySettingsView.as_view(), name="console-security-settings"),
    path("login-logs/", LoginAttemptLogListView.as_view({"get": "list"}), name="console-login-logs"),
]