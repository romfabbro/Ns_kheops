from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Unicode,
    text,
    Sequence,
    orm,
    func,
    select,
    bindparam,
    UniqueConstraint,
    event)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from traceback import print_exc
from datetime import datetime


from {{cookiecutter.repo_name}}.core import Base
from {{cookiecutter.repo_name}}.core.base_model import HasDynamicProperties
from {{cookiecutter.repo_name}}.utils.parseValue import dateParser


class Example(HasDynamicProperties, Base):

    __tablename__ = 'Example'

    moduleFormName = 'Form'
    moduleGridName = 'Grid'

    ID = Column(Integer, Sequence('Example__id_seq'), primary_key=True)
    Date = Column(DateTime, index=True, nullable=False)
    Name = Column(String(250))