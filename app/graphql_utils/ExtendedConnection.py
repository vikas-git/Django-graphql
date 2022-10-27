from unittest import result
import graphene
from django.db.models import Avg, Sum, Count, F, Window

class FilterNode(graphene.ObjectType):
    field_value = graphene.String()
    data = graphene.Int()

class PartitionNode(graphene.ObjectType):
    key = graphene.String()
    value = graphene.Float()


class ExtendedConnection(graphene.Connection):
    total_count = graphene.Int()
    edge_count = graphene.Int()
    count_by =  graphene.List(FilterNode, on_field=graphene.String())
    average_by =  graphene.List(FilterNode, on_field=graphene.String())
    sum_of =  graphene.List(FilterNode, on_field=graphene.String())
    partition_average_by =  graphene.List(PartitionNode, avg_by=graphene.String(), partition_by=graphene.String())
    partition_sum_by =  graphene.List(PartitionNode, sum_by=graphene.String(), partition_by=graphene.String())


    @property
    def get_model_object(root):
        return root.iterable.model

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)

    def resolve_count_by(root, info, on_field, **kwargs):
        model = root.get_model_object
        count_queryset = model.objects.values(on_field).annotate(count=Count(on_field))
        return [
            FilterNode(field_value=detail.get(on_field),
                                data=detail.get('count', 0))
            for detail in count_queryset
        ]

    def resolve_average_by(root, info, on_field, **kwargs):
        model = root.get_model_object
        avg_queryset = model.objects.aggregate(average=Avg(on_field))

        return [
            FilterNode(field_value=on_field, data=avg_queryset.get('average', 0))
        ]

    def resolve_sum_of(root, info, on_field, **kwargs):
        model = root.get_model_object
        queryset = model.objects.aggregate(sum=Sum(on_field))

        return [
            FilterNode(field_value=on_field, data=queryset.get('sum', 0))
        ]


    def resolve_partition_average_by(root, info, avg_by, partition_by, **kwargs):
        model = root.get_model_object
        queryset = model.objects.annotate(average=Window(
            expression=Avg(avg_by),
            partition_by=[F(partition_by)],
        )).distinct(partition_by)

        result = []
        for detail in queryset:
            detail = detail.__dict__
            result.append(PartitionNode(key=detail.get(partition_by),
                                value=detail.get('average', 0)))
        return result


    def resolve_partition_sum_by(root, info, sum_by, partition_by, **kwargs):
        model = root.get_model_object
        queryset = model.objects.annotate(sum=Window(
            expression=Sum(sum_by),
            partition_by=[F(partition_by)],
        )).distinct(partition_by)

        result = []
        for detail in queryset:
            detail = detail.__dict__
            result.append(PartitionNode(key=detail.get(partition_by),
                                value=detail.get('sum', 0)))
        return result

    class Meta:
        abstract = True