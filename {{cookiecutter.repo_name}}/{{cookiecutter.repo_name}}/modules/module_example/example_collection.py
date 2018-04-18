from sqlalchemy import (
    and_,
    func,
    select,
    exists,
    join,
    cast,
    not_,
    or_,
    DATE,
    outerjoin)
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import union_all

from {{cookiecutter.repo_name}}.core import Base
from {{cookiecutter.repo_name}}.core.base_collection import Query_engine, eval_
from . import Example


@Query_engine(Example)
class ExampleCollection:
    pass
