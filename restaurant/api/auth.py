from rest_framework.permissions import IsAuthenticated


class IsStaff(IsAuthenticated):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if has_permission:
            return bool(request.user.staff)
        return has_permission


class IsAdmin(IsStaff):
    def has_permission(self, request, view):

        has_permission = super().has_permission(request, view)
        if has_permission:
            return request.user.staff.is_admin
        return has_permission


class IsEmployee(IsStaff):
    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if has_permission:
            return request.user.staff.is_employee
        return has_permission
