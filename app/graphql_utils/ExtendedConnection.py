# schema.py
import graphene
from django.db.models import Avg, Sum, Count

class EmpFilterNode(graphene.ObjectType):
    field_value = graphene.String()
    data = graphene.Int()


class ExtendedConnection(graphene.Connection):
    total_count = graphene.Int()
    edge_count = graphene.Int()
    count_by =  graphene.List(EmpFilterNode, on_field=graphene.String())
    average_by =  graphene.List(EmpFilterNode, on_field=graphene.String())
    sum_of =  graphene.List(EmpFilterNode, on_field=graphene.String())

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)

    def resolve_count_by(root, info, on_field, **kwargs):
        model = root.iterable.model
        count_queryset = model.objects.values(on_field).annotate(count=Count(on_field))
        return [
            EmpFilterNode(field_value=detail.get(on_field),
                                data=detail.get('count', 0))
            for detail in count_queryset
        ]

    def resolve_average_by(root, info, on_field, **kwargs):
        model = root.iterable.model
        avg_queryset = model.objects.aggregate(average=Avg(on_field))

        return [
            EmpFilterNode(field_value=on_field, data=avg_queryset.get('average', 0))
        ]

    def resolve_sum_of(root, info, on_field, **kwargs):
        model = root.iterable.model
        queryset = model.objects.aggregate(sum=Sum(on_field))

        return [
            EmpFilterNode(field_value=on_field, data=queryset.get('sum', 0))
        ]


    class Meta:
        abstract = True
