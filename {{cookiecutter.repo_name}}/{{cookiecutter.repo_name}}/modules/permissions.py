from pyramid.security import (
    Allow,
    Authenticated,
    ALL_PERMISSIONS,
    NO_PERMISSION_REQUIRED,
    Everyone,
    Deny
)

context_permissions = {
    'examples': [
        (Allow, 'group:admin', ALL_PERMISSIONS),
        # (Allow, Authenticated, ALL_PERMISSIONS),
        (Allow, 'group:superUser', ('create', 'update', 'read')),
        (Allow, 'group:user', ('read'))
    ]
}
