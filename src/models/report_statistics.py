import os

from pynamodb.attributes import UnicodeAttribute, MapAttribute, NumberAttribute
from pynamodb.indexes import AllProjection

from models import BaseModel, BaseGSI
from helpers.constants import CAASEnv


class CustomerNameTriggeredAtIndex(BaseGSI):
    class Meta:
        index_name = 'customer_name-triggered_at-index'
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    customer_name = UnicodeAttribute(hash_key=True)
    triggered_at = UnicodeAttribute(range_key=True)


class StatusIndex(BaseGSI):
    class Meta:
        index_name = 'status-index'
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    status = UnicodeAttribute(hash_key=True)


class ReportStatistics(BaseModel):
    class Meta:
        table_name = 'CaaSReportStatistics'
        region = os.environ.get(CAASEnv.AWS_REGION)

    id = UnicodeAttribute(hash_key=True)
    triggered_at = UnicodeAttribute(range_key=True)
    attempt = NumberAttribute(null=True, default=1)
    user = UnicodeAttribute(null=True)
    level = UnicodeAttribute(null=True)
    type = UnicodeAttribute(null=True)
    status = UnicodeAttribute(null=True)  # FAILED, SUCCEEDED, PENDING, RETRIED, DUPLICATE
    customer_name = UnicodeAttribute(null=True)
    tenant = UnicodeAttribute(null=True)
    reason = UnicodeAttribute(null=True)
    event = MapAttribute(default=dict)

    customer_name_triggered_at_index = CustomerNameTriggeredAtIndex()
    status_index = StatusIndex()
