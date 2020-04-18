from views.user import user_schema

admin_verification_schema = {
    'type': 'object',
    'properties': {
        'user_id': {
            'type': 'string',
            'pattern': r'^\d{16,20}$'
        },
        'guild_id': {
            'type': 'string',
            'pattern': r'^\d{16,20}$'
        }
    },
    'required': ['user_id', 'guild_id'],
    'additionalProperties': False
}

user_verification_schema = {
    'type': 'object',
    'properties': {
        'user': user_schema
    },
    'additionalProperties': False
}