club_schema = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
            'minLength': 3,
            'maxLength': 64
        },
        'permalink': {
            'type': 'string',
            'minLength': 3,
            'maxLength': 20
        },
        'description': {
            'type': 'string',
            'minLength': 10
        },
        'email': {
            'type': 'string',
            'format': 'email'
        },
        'website': {
            'type': 'string',
            'format': 'uri'
        },
        'discord_id': {
            'type': 'string',
            'pattern': r'^\d+$',
            'minLength': 16,
            'maxLength': '20'
        }
    },
    'required': ['name', 'permalink', 'description', 'email', 'website'],
    'additionalProperties': False
}