import graphene
from graphene_django.types import DjangoObjectType
from api_app.models import Employee
from api_app.filters import EmployeeFilter
from graphql_utils.ExtendedConnection import ExtendedConnection


class EmployeeNode(DjangoObjectType):
    # empID = graphene.Field(graphene.Int)

    class Meta:
        model = Employee
        interfaces = (graphene.Node,)
        fields = "__all__"
        filterset_class = EmployeeFilter
        connection_class = ExtendedConnection
