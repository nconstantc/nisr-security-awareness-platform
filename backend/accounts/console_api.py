from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .console_serializers import (
    DepartmentAdminSerializer,
    EmployeeAdminSerializer,
    EmployeeRoleSerializer,
    LdapSettingsSerializer,
    LoginAttemptLogSerializer,
    SecuritySettingsSerializer,
)
from .models import Department, LdapSettings, LoginAttemptLog, SecuritySettings, User
from .permissions import IsSuperAdmin
from .services import reset_user_password


class DepartmentListView(generics.ListCreateAPIView):
    """List and create departments"""
    queryset = Department.objects.all().order_by("name")
    serializer_class = DepartmentAdminSerializer
    permission_classes = [IsAdminUser]


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete a department"""
    queryset = Department.objects.all().order_by("name")
    serializer_class = DepartmentAdminSerializer
    permission_classes = [IsAdminUser]


class EmployeeListView(generics.ListCreateAPIView):
    serializer_class = EmployeeAdminSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = User.objects.filter(is_active=True).select_related("department").order_by("full_name")
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(full_name__icontains=search)
        return qs

    def create(self, request, *args, **kwargs):
        # Add any custom logic for creating employees if needed
        return super().create(request, *args, **kwargs)


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and remove an employee.

    "Delete" is a soft-delete (is_active=False), not a real row delete - the employee is
    referenced by wave assignments, quiz attempts, badges, phishing results, and login logs,
    and hard-deleting would either cascade-destroy that audit history or fail outright
    depending on each relation's on_delete. Every other employee endpoint already filters on
    is_active=True, so this keeps that convention consistent.
    """

    serializer_class = EmployeeAdminSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all().select_related("department")

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active"])


class EmployeeResetPasswordView(APIView):
    """Reset employee password"""
    permission_classes = [IsSuperAdmin]

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk, is_active=True)
        temp_password = reset_user_password(user)
        return Response({"temp_password": temp_password})


class EmployeeRoleView(APIView):
    """Change employee role"""
    permission_classes = [IsSuperAdmin]

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk, is_active=True)
        if user == request.user and request.data.get("role") != User.ROLE_ADMIN:
            return Response(
                {"detail": "You cannot remove admin rights from yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = EmployeeRoleSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(EmployeeAdminSerializer(user).data)


class LdapSettingsView(APIView):
    """LDAP/AD settings"""
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        return Response(LdapSettingsSerializer(LdapSettings.get_solo()).data)

    def patch(self, request):
        config = LdapSettings.get_solo()
        serializer = LdapSettingsSerializer(config, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LdapTestConnectionView(APIView):
    """Test LDAP connection"""
    permission_classes = [IsSuperAdmin]

    def post(self, request):
        import ldap

        server_uri = (request.data.get("server_uri") or "").strip()
        bind_dn = request.data.get("bind_dn") or ""
        bind_password = request.data.get("bind_password") or ""
        start_tls = bool(request.data.get("start_tls"))

        if not bind_password:
            saved = LdapSettings.get_solo()
            if saved.bind_dn == bind_dn:
                bind_password = saved.bind_password

        if not server_uri:
            return Response({"ok": False, "detail": "Server URI is not specified"}, status=status.HTTP_400_BAD_REQUEST)

        conn = ldap.initialize(server_uri)
        conn.set_option(ldap.OPT_REFERRALS, 0)
        conn.set_option(ldap.OPT_NETWORK_TIMEOUT, 5)
        try:
            if start_tls:
                conn.start_tls_s()
            conn.simple_bind_s(bind_dn, bind_password)
            return Response({"ok": True, "detail": "Connection and bind successful"})
        except ldap.LDAPError as exc:
            detail = exc.args[0].get("desc") if exc.args and isinstance(exc.args[0], dict) else str(exc)
            return Response({"ok": False, "detail": f"Connection error: {detail}"})
        finally:
            try:
                conn.unbind_s()
            except ldap.LDAPError:
                pass


class SecuritySettingsView(APIView):
    """Security settings"""
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        return Response(SecuritySettingsSerializer(SecuritySettings.get_solo()).data)

    def patch(self, request):
        config = SecuritySettings.get_solo()
        serializer = SecuritySettingsSerializer(config, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAttemptLogListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Login attempt log - last 200 entries"""
    queryset = LoginAttemptLog.objects.order_by("-created_at")[:200]
    serializer_class = LoginAttemptLogSerializer
    permission_classes = [IsSuperAdmin]