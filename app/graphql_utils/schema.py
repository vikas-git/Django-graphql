import graphene
from graphql_utils.query import QueryAll
"""
    Schema for handling all Queries & Mutations
"""
schema = graphene.Schema(query=QueryAll)
