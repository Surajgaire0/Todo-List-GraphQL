import graphene
from graphql_auth.schema import UserQuery, MeQuery
from todoapp.schema import Query as TodoQuery, Mutation as TodoMutation
from users.schema import AuthMutation


class Query(TodoQuery, UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(TodoMutation, AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
