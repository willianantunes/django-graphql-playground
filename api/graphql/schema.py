import graphene

from api.graphql.mutations import Mutations
from api.graphql.query import QueryDefinition


class Query(QueryDefinition, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
