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
            'maxLength': 20
        }
    },
    'required': ['name', 'permalink', 'description', 'email', 'website', 'discord_id'],
    'additionalProperties': False
}

club_guild_update_schema = {
    'type': 'object',
    'properties': {
        'key': {
            'type': 'string',
            'enum': ['admin_role_id', 'verified_role_id', 'admin_channel_id']
        },
        'value': {
            'type': 'string',
            'pattern': r'^\d+$',
            'minLength': 16,
            'maxLength': 20
        }
    },
    'required': ['key', 'value'],
    'additionalProperties': False
}