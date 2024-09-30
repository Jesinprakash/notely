from rest_framework.permissions import BasePermission

class OwnerOnly(BasePermission):

    def has_object_permission(self, request, view, obj):  #here obj is which model

        return request.user==obj.owner
    

    