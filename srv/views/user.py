member_schema = {
    'type': 'object',
    'properties': {
        'zid': {
            'type': 'string',
            'pattern': '^z[0-9]{7}$'
        },
        'email': {
            'type': 'string',
            'format': 'email'
        },
        'phone': {
            'type': 'string',
            'pattern': '^04[0-9]{8}$'
        },
        'given_name': {
            'type': 'string',
            'minLength': 1
        },
        'family_name': {
            'type': 'string',
            'minLength': 1
        },
        'arc_member': {
            'type': 'boolean'
        }
    },
    'required': ['given_name', 'family_name', 'arc_member'],
    'anyOf': [
        {'required': ['zid']},
        {'required': ['email', 'phone']}
    ]
}