import graphene

from app.graphql.mutations import Mutations
from app.graphql.query import QueryDefinition


class Query(QueryDefinition, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
