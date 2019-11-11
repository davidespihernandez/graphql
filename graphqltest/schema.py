import graphene

from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphqltest.models import Master, Detail, Status as MasterStatus


class StatusDescription(graphene.Enum):
    OPEN = MasterStatus.OPEN.value
    CLOSED = MasterStatus.CLOSED.value


class MasterType(DjangoObjectType):
    status = StatusDescription()

    class Meta:
        model = Master
        filter_fields = ['name', 'deleted', 'status', 'details']


class DetailType(DjangoObjectType):
    class Meta:
        model = Detail


class MasterNode(DjangoObjectType):
    status = StatusDescription()

    class Meta:
        model = Master
        filter_fields = ['name', 'deleted', 'status', 'details']
        interfaces = (relay.Node,)


class DetailNode(DjangoObjectType):
    class Meta:
        model = Detail
        # more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'amount': ['gt', 'gte', 'lt', 'lte'],
            'master__name': ['exact'],
        }
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    master = relay.Node.Field(MasterNode)
    all_master = DjangoFilterConnectionField(MasterNode)

    detail = relay.Node.Field(DetailNode)
    all_details = DjangoFilterConnectionField(DetailNode)
