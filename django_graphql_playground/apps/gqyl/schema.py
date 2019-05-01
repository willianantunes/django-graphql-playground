import graphene

from django_graphql_playground.apps.gqyl.mutations import Mutations
from django_graphql_playground.apps.gqyl.query import QueryDefinition


class Query(QueryDefinition, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
