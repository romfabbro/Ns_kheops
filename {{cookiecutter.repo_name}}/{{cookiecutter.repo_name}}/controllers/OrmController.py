import types
from functools import wraps
from sqlalchemy import (Column,
                        ForeignKey,
                        String,
                        Integer,
                        Float,
                        Boolean,
                        DateTime,
                        select,
                        join,
                        func,
                        not_,
                        exists,
                        event,
                        Table,
                        Index,
                        UniqueConstraint,
                        Table,
                        text,
                        bindparam,
                        insert,
                        desc)
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import *

from ..core import Base, dbConfig
from ..core.base_model import HasDynamicProperties, HasStaticProperties
from ..core.base_collection import Query_engine


class OrmFactory(object):
    __allORMClass__ = {}

    staticTypeDict = {'String': String,
                      'Float': Float,
                      'Integer': Integer,
                      'DateTime': DateTime,
                      'Boolean': Boolean
                      }

    def __init__(self, objList=[]):
        self.conf = objList
        for obj in objList:
            self.buildClass(obj)

    def __getattr__(self, attr):
        if self.getClass(attr):
            return self.getClass(attr)
        if self.findOrmEntity(attr):
            return self.findOrmEntity(attr)

    @staticmethod
    def findOrmEntity(tablename):
        filterEntity = list(filter(lambda e: hasattr(
            e, '__tablename__') and e.__tablename__ == tablename, Base._decl_class_registry.values()))
        if filterEntity:
            return filterEntity[0]
        else:
            return None

    def buildClass(self, dict_):
        model = {}
        model['__tablename__'] = dict_['__tablename__']
        model = self.setStaticProperties(model, dict_['properties']['statics'])

        if('__classname__' in dict_):
            classname = dict_['__classname__']
        else:
            classname = dict_['__tablename__'].title()

        if dict_['properties'].get('dynamics', None):
            dbObject = type(classname, (HasDynamicProperties, Base, ), model)
            if 'history_track' in dict_:
                dbObject.history_track = dict_.get('history_track')

            self.setDBConfTypes(dbObject, dict_)
        else:
            model['ID'] = Column(Integer, primary_key=True)
            dbObject = type(classname, (HasStaticProperties, Base, ), model)

        self.setCollection(dbObject)
        self.add(dbObject)

    def setCollection(self, dbObject):
        @Query_engine(dbObject)
        class Collection:
            pass
        dbObject.Collection = type('Collection'+dbObject.__tablename__, (Collection, ), {})

    def setStaticProperties(self, model, properties):
        for prop in properties:
            if prop.get('foreign_key', None):
                model[prop['name']] = Column(prop['name'], self.getCType(
                    prop), ForeignKey(prop.get('foreign_key')))
            else:
                model[prop['name']] = Column(prop['name'], self.getCType(prop))
        return model

    def getCType(self, property):
        if property.get('clength', None):
            l = property['clength']
            return self.staticTypeDict[property['ctype']](l)
        else:
            return self.staticTypeDict[property['ctype']]

    def getClass(self, classname):
        return self.__allORMClass__.get(classname, None)

    def setDBConfTypes(self, curORMclass, model):
        @event.listens_for(curORMclass, 'mapper_configured')
        def setDBConfTypes(mapper, class_):
            if curORMclass:
                self.insertConfTypes(curORMclass, model)
                self.insertConfDynProp(curORMclass, model)
                self.insertConfType_DynProp(curORMclass, model)
                self.setRelationships(curORMclass, model)

    def setRelationships(self, dbObject, model):
        confProperties = model.get('properties', {})
        session = dbConfig['dbSession']()

        for prop in confProperties.get('statics', []):
            if prop.get('foreign_key', None):
                tablename = prop.get('foreign_key').split('.')[0]
                entity = self.findOrmEntity(tablename)
                setattr(dbObject, '_' + entity.__name__, relationship(entity))

    def insertConfTypes(self, dbObject, model):
        modelType = dbObject.TypeClass
        session = dbConfig['dbSession']()
        for _type in model.get('types', []):
            stmt = select([func.count(modelType.ID)]).where(
                modelType.Name == _type)
            typeExists = session.execute(stmt).scalar()

            if not typeExists:
                insert_stmt = insert(modelType).values({'Name': _type})
                session.execute(insert_stmt)
        session.commit()
        session.close()

    def insertConfDynProp(self, dbObject, model):
        modelProperties = dbObject.TypeClass.PropertiesClass
        confProperties = model.get('properties', {})
        session = dbConfig['dbSession']()
        for prop in confProperties.get('dynamics', []):
            stmt = select([func.count(modelProperties.ID)]).where(
                modelProperties.Name == prop['name'])
            typeExists = session.execute(stmt).scalar()

            if not typeExists:
                insert_stmt = insert(modelProperties).values(
                    {'Name': prop['name'], 'TypeProp': prop['ctype']})
                session.execute(insert_stmt)
        session.commit()
        session.close()

    def insertConfType_DynProp(self, dbObject, model):
        modelProperties = dbObject.TypeClass.PropertiesClass
        modelType = dbObject.TypeClass
        modelTypeProperties = dbObject.TypeClass.TypePropertiesClass

        session = dbConfig['dbSession']()
        types = session.execute(select([modelType])).fetchall()
        properties = session.execute(select([modelProperties])).fetchall()
        typeProperties = session.execute(
            select([modelTypeProperties])).fetchall()

        valuesToInsert = []
        for _type, props in model.get('types', []).items():
            curType = list(filter(lambda t: t['Name'] == _type, types))[0]
            for prop in props:
                curProp = list(
                    filter(lambda p: p['Name'] == prop, properties))[0]
                linkExists = list(filter(lambda x: x[dbObject.fk_table_type_name] == curType['ID']
                                         and x[dbObject.fk_table_DynProp_name] == curProp['ID'], typeProperties))
                if not linkExists:
                    valuesToInsert.append(
                        {dbObject.fk_table_type_name: curType['ID'], dbObject.fk_table_DynProp_name: curProp['ID']})

        if valuesToInsert:
            insert_stmt = insert(modelTypeProperties).values(valuesToInsert)
            session.execute(insert_stmt)

        session.commit()
        session.close()

    def add(self, dbObject):
        self.__allORMClass__[dbObject.__name__] = dbObject

    @staticmethod
    def patch(myClass, methodType=None):
        methodTypeDict = {'classmethod': classmethod,
                          'staticmethod': staticmethod}
        wrappingMethod = methodTypeDict.get(methodType, None)

        def real_decorator(function):
            if not wrappingMethod:
                setattr(myClass, function.__name__, function)
            else:
                setattr(myClass, function.__name__, wrappingMethod(function))
        return real_decorator
