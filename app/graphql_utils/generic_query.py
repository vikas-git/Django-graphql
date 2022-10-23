
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_utils.nodes import *


class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):
    @classmethod
    def resolve_queryset(cls, connection, iterable, info, args, filtering_args, filterset_class):
        qs = super().resolve_queryset(
            connection, iterable, info, args, filtering_args, filterset_class
        )
        order = args.get("orderBy", None)
        if order:
            # if isinstance(order, str):
            #     snake_order = order
            # else:
            #     snake_order = [o for o in order]

            snake_order = order
            # annotate counts for ordering
            for order_arg in snake_order:
                order_arg = order_arg.lstrip("-")
                annotation_name = f"annotate_{order_arg}"
                annotation_method = getattr(qs, annotation_name, None)
                if annotation_method:
                    qs = annotation_method()

            # override the default distinct parameters
            # as they might differ from the order_by params
            qs = qs.order_by(*snake_order).distinct()

        return qs



class Query(object):
    # employee = Node.Field(EmployeeNode)
    all_employee = OrderedDjangoFilterConnectionField(
        EmployeeNode,
        orderBy=graphene.List(of_type=graphene.String)
    )
