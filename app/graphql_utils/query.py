import graphene
from .generic_query import Query
from graphene_django.debug import DjangoDebug


class QueryAll(Query, graphene.ObjectType):
    pass
    # debug = graphene.Field(DjangoDebug, name="_debug")
