from rest_framework import permissions

class IsSuperAdminPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        # ip_addr = request.META['REMOTE_ADDR']
        # blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
        has_permission=request.user.role=='superadmin'
        return has_permission
    
    
class IsAdminPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """
    # CHECK ORGANIZATION
    def has_permission(self, request, view):
        has_permission=request.user.role=='admin'
        return has_permission