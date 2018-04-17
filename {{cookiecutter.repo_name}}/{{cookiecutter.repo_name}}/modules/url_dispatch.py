
def add_routes(config):

    # Security routes
    config.add_route('security/login', 'ecoReleve-Core/security/login')
    config.add_route('security/logout', 'ecoReleve-Core/security/logout')
    config.add_route('security/has_access',
                     'ecoReleve-Core/security/has_access')