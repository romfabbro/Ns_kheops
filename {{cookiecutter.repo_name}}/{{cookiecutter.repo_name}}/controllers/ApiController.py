
# # ###
# # TODO: create ApiController
# # ###


# # ###
# # TODO: create ApiController
# # ###
from ..core.base_resource import *
from ..modules.permissions import context_permissions


class ApiFactory(object):

    __all_resource_class__ = {}

    def __init__(self, ModelFactory, config):
        from ..core import RootCore
        self.RootCore = RootCore
        self.ModelFactory = ModelFactory
        for obj in config:
            self.buildResource(obj)

    def buildResource(self, obj):
        obj_model = getattr(self.ModelFactory, obj['model'])
        CollectionResource = self.getCollectionResource(obj, obj_model)

        if obj['parent'] == 'root':
            self.RootCore.children.append((obj['route_name'], CollectionResource))

    def getCollectionResource(self, obj, obj_model):
        ItemResource = self.getItemResource(obj, obj_model)

        class CollectionResource(DynamicObjectCollectionResource):
            Collection = obj_model.Collection
            model = obj_model
            moduleFormName = obj.get('moduleFormName', None)
            moduleGridName = obj.get('moduleGridName', None)

            children = [('{int}', ItemResource)]
            __acl__ = context_permissions[obj.get('permission_name')]

        return type(obj_model.__name__+'CollectionResource', (CollectionResource, ), {})

    def getItemResource(self, obj, obj_model):

        class ItemResource(DynamicObjectResource):
            model = obj_model

        return type(obj_model.__name__+'Resource', (ItemResource, ), {})


