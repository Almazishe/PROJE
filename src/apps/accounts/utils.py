def check_user_data(email, first_name, last_name, phone_number) -> dict:
    ''' Check if Account data is valid '''

    error_template = 'User account must have'

    data = {
        'errors': {},
        'status': 0,                    # 0 - SUCCESS |  2 - ERROR
    }

    if not email:
        data['errors']['email'] = f'{error_template} email.'
        data['status'] = 2
    if not first_name:
        data['errors']['first_name'] =f'{error_template} first name.'
        data['status'] = 2
    if not last_name:
        data['errors']['last_name'] = f'{error_template} last name.'
        data['status'] = 2
    if not phone_number:
        data['errors']['phone_number'] = f'{error_template} phone number.'
        data['status'] = 2
    
    return data
