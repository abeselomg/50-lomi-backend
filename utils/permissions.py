from rest_framework import permissions
from users.models import OrganizationUser
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
    Global permission check for Admins in Orgs.
    """
    
    
    message = 'Permission Denied. User needs to have an Admin role in the specified organization.'
    def has_permission(self, request, view):

        if request.user.role=='admin':
            if OrganizationUser.objects.filter(user=request.user).exists():
                
                #NOT A FINAL SOLUTION.
                if request.method in ["GET","PATCH", "DELETE"]:
                    return True
                
                org_id=OrganizationUser.objects.get(user=request.user).organization.id
                org = request.data['organizationId'] 
                if str(org_id)==org:
                    return True
            
        return False
    

class IsEventOrgPermission(permissions.BasePermission):
    """
    Global permission check for Admins in Orgs.
    """
    
    
    message = 'Permission Denied. User needs to have an Admin role in the specified organization.'
    def has_permission(self, request, view):

        if request.user.role=='event_org':
            if OrganizationUser.objects.filter(user=request.user).exists():
                
                #NOT A FINAL SOLUTION.
                if request.method in ["GET","PATCH", "DELETE"]:
                    return True
                
                org_id=OrganizationUser.objects.get(user=request.user).organization.id
                org = request.data['organizationId'] 
                if str(org_id)==org:
                    return True
            
        return False
    
