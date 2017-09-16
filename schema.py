# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import Car as CarModel, Model as ModelModel, get_brand, get_model, get_brands


class Brand(graphene.ObjectType):
    name = graphene.String()

    # models = graphene.List(Model)

    class Meta:
        interfaces = (relay.Node,)

    @classmethod
    def get_node(cls, info, id):
        return get_brand(id)

    """
    def resolve_models(self, info, *args, **kwargs):
        return get_model(info, self.id)
    """


class Model(SQLAlchemyObjectType):
    brand = graphene.Field(Brand)

    class Meta:
        model = ModelModel
        interfaces = (relay.Node,)

    def resolve_brand(self, info, *args, **kwargs):
        return get_brand(self.brand_id)


class Car(SQLAlchemyObjectType):
    class Meta:
        model = CarModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    cars = graphene.List(Car)

    models = graphene.List(Model)
    model = graphene.Field(Model)

    brands = graphene.List(Brand)
    brand = graphene.Field(Brand, id=graphene.String(), )

    def resolve_cars(self, info, *args, **kwargs):
        query = Car.get_query(info)
        return query.all()

    def resolve_models(self, info, *args, **kwargs):
        query = Model.get_query(info)
        return query.all()

    def resolve_model(self, info, *args, **kwargs):
        id = kwargs.get('id')
        return get_model(info, id)

    def resolve_brands(self, info, *args, **kwargs):
        return get_brands()

    def resolve_brand(self, info, *args, **kwargs):
        return get_brand(info["id"])


schema = graphene.Schema(query=Query)
