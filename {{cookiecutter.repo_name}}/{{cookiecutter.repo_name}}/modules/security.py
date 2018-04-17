from pyramid.security import forget, NO_PERMISSION_REQUIRED
from pyramid.view import view_config


route_prefix = 'security/'


@view_config(
    route_name=route_prefix+'logout',
    permission=NO_PERMISSION_REQUIRED,)
def logout(request):
    forget(request)
    return request.response


@view_config(route_name=route_prefix+'has_access')
def has_access(request):
    return request.response
