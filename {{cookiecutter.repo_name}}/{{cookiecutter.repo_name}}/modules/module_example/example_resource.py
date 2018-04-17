import json
import itertools
from datetime import datetime
import pandas as pd
from sqlalchemy import select, and_, join
from sqlalchemy.exc import IntegrityError

from {{cookiecutter.repo_name}}.core import RootCore
from {{cookiecutter.repo_name}}.core.base_resource import DynamicObjectResource, DynamicObjectCollectionResource

from .example_collection import ExampleCollection
from .example_model import Example
from ..permissions import context_permissions


class ExampleResource(DynamicObjectResource):

    model = Example
    # __acl__ = context_permissions['Examples'] #inherit acl from parent


class ExamplesResource(DynamicObjectCollectionResource):

    Collection = ExampleCollection
    model = Example
    moduleFormName = 'ExampleForm'
    moduleGridName = 'ExampleGrid'

    children = [('{int}', ExampleResource)]

    __acl__ = context_permissions['examples']


RootCore.children.append(('examples', ExamplesResource))
