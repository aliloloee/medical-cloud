# from rest_framework import permissions


# class IsOwner(permissions.BasePermission) :
#     """Allow users to edit their own profile only"""

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS :
#             return True
        
#         return obj.user == request.user 

