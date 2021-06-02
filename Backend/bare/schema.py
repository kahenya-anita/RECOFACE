import graphene
import faces.schema

class Query(faces.schema.Query, graphene.ObjectType):
    pass


class Mutation(faces.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(mutation=Mutation, query=Query)