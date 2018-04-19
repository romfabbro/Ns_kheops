from pyramid.security import (
    Allow,
    Authenticated,
    ALL_PERMISSIONS,
    Everyone,
    Deny
)
from pyramid.view import view_config, view_defaults

from .init_db import Base, BaseExport, dbConfig, get_redis_con, ModelFactory, storageConf
from .base_model import *
from .base_view import *
from .base_resource import *
from .configuration_model import *
from ..controllers.ApiController import ApiFactory

api_root = '{{cookiecutter.api_root_name}}'


def ini_resource_factory():
    global ResourceFactory
    try:
        ResourceFactory = ApiFactory(ModelFactory, storageConf['api_objects'])
    except:
        pass


class SecurityRoot(Resource):
    __acl__ = [
        (Allow, Authenticated, 'read'),
        (Allow, Authenticated, 'all'),
        (Allow, 'group:admin', 'admin'),
        (Allow, 'group:admin', 'superUser'),
        (Allow, 'group:admin', 'all'),
        (Allow, 'group:superUser', 'superUser'),
        (Allow, 'group:superUser', 'all')
    ]

    def __init__(self, request):
        Resource.__init__(self, ref='', parent=None)
        self.request = request

    def __getitem__(self, item):
        if item == api_root:
            return RootCore(item, self)
        else:
            raise KeyError


class RootCore(Resource):

    children = []

    def retrieve(self):
        return {'next items': self}


@view_defaults(context=SecurityRoot)
class HomeView:

    def __init__(self, request, context):
        self.request = request
        self.context = context

    @view_config(request_method='GET', renderer='json', permission='read')
    def home(self):
        return 'hello'
