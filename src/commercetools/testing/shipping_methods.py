import datetime
import typing
import uuid

from commercetools import schemas, types
from commercetools.testing.abstract import BaseModel, ServiceBackend


class ShippingMethodsModel(BaseModel):
    _resource_schema = schemas.ShippingMethodSchema

    def _create_from_draft(
        self, obj: types.ShippingMethodDraft, id: typing.Optional[str] = None
    ) -> types.ShippingMethod:
        object_id = str(uuid.UUID(id) if id is not None else uuid.uuid4())
        return types.ShippingMethod(
            id=str(object_id),
            key=obj.key,
            version=1,
            created_at=datetime.datetime.now(),
            last_modified_at=datetime.datetime.now(),
            name=obj.name,
            description=obj.description,
            tax_category=obj.tax_category,
            zone_rates=obj.zone_rates,
            is_default=obj.is_default,
            predicate=obj.predicate,
        )


class ShippingMethodsBackend(ServiceBackend):
    service_path = "shipping-methods"
    model_class = ShippingMethodsModel
    _schema_draft = schemas.ShippingMethodDraftSchema
    _schema_query_response = schemas.ShippingMethodPagedQueryResponseSchema

    def urls(self):
        return [
            ("^$", "GET", self.query),
            ("^$", "POST", self.create),
            ("^(?P<id>[^/]+)$", "GET", self.get_by_id),
            ("^(?P<id>[^/]+)$", "POST", self.update_by_id),
        ]
