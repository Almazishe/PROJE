from rest_framework.permissions import BasePermission


class IsSelfOrAdmin(BasePermission):
    """ Check of User is admin or he is accessing to his own data """

    message = 'It\s not your account or you are not \'Admin\'.'

    def has_object_permission(self, request, view, obj):
        print(obj.email)
        print(request.user.email)
        return bool(request.user and (request.user == obj or request.user.is_staff == True))