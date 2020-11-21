from rest_framework.serializers import ValidationError


STATUS_ERROR = '02'
STATUS_SUCCESS = '00'




def check_user_data(email, first_name, last_name, phone_number) -> dict:
    ''' Check if Account data is valid '''

    error_template = 'User account must have'

    data = {
        'errors': {},
        'status': STATUS_SUCCESS,
    }

    if not email:
        data['errors']['email'] = f'{error_template} email.'
        data['status'] = STATUS_ERROR
    if not first_name:
        data['errors']['first_name'] =f'{error_template} first name.'
        data['status'] = STATUS_ERROR
    if not last_name:
        data['errors']['last_name'] = f'{error_template} last name.'
        data['status'] = STATUS_ERROR
    if not phone_number:
        data['errors']['phone_number'] = f'{error_template} phone number.'
        data['status'] = STATUS_ERROR
    
    return data


def check_passwords(password1, password2):
    ''' CHECK IF 2 PASSWORDS ARE EQUAL OR NOT NONE '''

    data = {
        'errors': {},
        'password': None,
        'status': STATUS_SUCCESS, 
    }

    if password1 is not None and password2 is not None:
        if password1 == password2:
            data['password'] = password1
        else:
            data['errors']['password2'] = 'Passwords are not equal.' 
            data['status'] = STATUS_ERROR
    else:
        data['errors']['password'] = 'password1 or password2 have not been declared.' 
        data['status'] = STATUS_ERROR
    
    return data