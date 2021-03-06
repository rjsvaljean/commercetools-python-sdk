import datetime
import typing
import uuid

from commercetools import schemas, types
from commercetools.testing.abstract import BaseModel, ServiceBackend


class ExtensionsModel(BaseModel):
    _resource_schema = schemas.ExtensionSchema

    def _create_from_draft(
        self, obj: types.ExtensionDraft, id: typing.Optional[str] = None
    ) -> types.Extension:
        object_id = str(uuid.UUID(id) if id is not None else uuid.uuid4())
        return types.Extension(
            id=str(object_id),
            version=1,
            created_at=datetime.datetime.now(),
            last_modified_at=datetime.datetime.now(),
            key=obj.key,
            destination=obj.destination,
            triggers=obj.triggers,
        )


class ExtensionsBackend(ServiceBackend):
    service_path = "extensions"
    model_class = ExtensionsModel
    _schema_draft = schemas.ExtensionDraftSchema
    _schema_query_response = schemas.ExtensionPagedQueryResponseSchema

    def urls(self):
        return [
            ("^$", "GET", self.query),
            ("^$", "POST", self.create),
            ("^(?P<id>[^/]+)$", "GET", self.get_by_id),
            ("^(?P<id>[^/]+)$", "POST", self.update_by_id),
            ("^(?P<id>[^/]+)$", "DELETE", self.delete_by_id),
            ("^key=(?P<key>[^/]+)$", "DELETE", self.delete_by_key),
        ]
