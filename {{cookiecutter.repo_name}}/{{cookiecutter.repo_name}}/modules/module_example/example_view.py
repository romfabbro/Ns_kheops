from pyramid.view import view_config, view_defaults

from {{cookiecutter.repo_name}}.core.base_view import CRUDCommonView, RestCollectionView
from .example_resource import ExampleResource, ExamplesResource


@view_defaults(context=ExamplesResource)
class ExamplesView(RestCollectionView):

    @view_config(name='examples_action', request_method='GET', renderer='json')
    def example_tzzez(self):
        return self.context.example_route()
