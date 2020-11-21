from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import *

from apps.accounts.utils import STATUS_ERROR
from apps.accounts.utils import STATUS_SUCCESS
from apps.accounts.email import send_activation_email
from apps.accounts.email import activate_account

from .serializers import AccountCreateSerializer
from .serializers import AccountRUDSerializer


@api_view(['POST'])
@permission_classes([AllowAny,])
def confirm_account(request):
    ''' WHEN PRESSED CONFIRM LINK FROM FRONTEND '''
    response_data = {}

    if request.method == 'POST':
        data = request.data
        try:
            uidb64 = data['uid']
            token = data['token']

            activate_account(uidb64, token)                                 # ACTIVATE ACCOUNT

            response_data['success'] = 'Account activated successfully.'
            return Response(
                data=response_data,
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            response_data['errors'] = e.args
            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        response_data['errors'] = {
            'request-method': 'Only POST  request\'s are accepted.'
        }

    return Response(
        data=response_data,
        status=status.HTTP_400_BAD_REQUEST
    )



@api_view(('POST', 'GET'))
@permission_classes((AllowAny,))
def users(request):
    ''' CREATE | LIST USERS '''

    response_data = {}

    if request.method == 'POST':
        ''' IF CREATING USER '''

        data = request.data
        try:
            serializer = AccountCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                
                user = serializer.instance
                send_activation_email(user)                                             # SEND ACTIVATION EMAIL

                response_data['success'] = 'User created successfully.'
                return Response(
                    data=response_data,
                    status=status.HTTP_201_CREATED,
                )
            else:
                response_data['errors'] = serializer.errors
                return Response(
                    data=response_data,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            response_data['errors'] = e.args 
            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST,
            )
    elif request.method == 'GET':
        users = User.objects.all()
        serializer = AccountCreateSerializer(users, many=True)
        response_data['users'] = serializer.data
        response_data['success'] = 'Uses got successfully.'
        return Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )
        
    else:
        response_data['errors'] = {
            'request-method': 'Only GET | POST  request\'s are accepted.'
        }

    return Response(
        data=response_data,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(('GET', 'PUT', 'DELETE',))
@permission_classes([IsAuthenticated,])
def user_RUD(request, uuid=None):
    ''' User Account API view GET | UPDATE | DELETE'''
    response_data = {}

    if request.method == 'PUT':
        ''' IF UPDATING USER '''
        try:
            data = request.data
            
            user = User.get_user_by_uuid(uuid)
            if user is not None:
                serializer = AccountRUDSerializer(data=data, instance=user, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    response_data['success'] = 'User updated successfully.'
                    return Response(
                        data=response_data,
                        status=status.HTTP_200_OK,
                    )
                else:
                    response_data['errors'] = serializer.errors
                    return Response(
                        data=response_data,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                response_data['errors'] = {
                    'detail': "No user with such UUID."
                }

                return Response(
                    data=response_data,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            response_data['errors'] = {} 
            for i in range(len(e.args)):
                response_data['errors'].update(e.args[i]) 
            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST,
            )
    elif request.method == 'GET':
        user = User.get_user_by_uuid(uuid)
        if user is not None:
            serializer = AccountRUDSerializer(user)
            response_data['detail'] = serializer.data
            response_data['success'] = 'User account detail got successfully.'
            return Response(
                data=response_data,
                status=status.HTTP_200_OK,
            )
        else:
            response_data['errors'] = {
                'detail': 'No user with such UUID.'
            }

            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    else:
        response_data['errors'] = {
            'request-method': 'Only GET | PUT | DELETE  request\'s are accepted.'
        }

    return Response(
        data=response_data,
        status=status.HTTP_400_BAD_REQUEST
    )
