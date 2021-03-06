import typing
from typing import List, Optional

from marshmallow import fields

from commercetools import schemas, types
from commercetools.services import abstract
from commercetools.typing import OptionalListStr

__all__ = ["CartService"]


class CartDeleteSchema(abstract.AbstractDeleteSchema):
    data_erasure = fields.Bool(data_key="dataErause", required=False)


class CartQuerySchema(abstract.AbstractQuerySchema):
    pass


class CartService(abstract.AbstractService):
    def get_by_id(self, id: str) -> Optional[types.Cart]:
        return self._client._get(f"carts/{id}", {}, schemas.CartSchema)

    def get_by_customer_id(self, customer_id: str) -> types.Cart:
        params = {"customerId": customer_id}
        return self._client._get(f"carts/", params, schemas.CartSchema)

    def query(
        self,
        where: OptionalListStr = None,
        sort: OptionalListStr = None,
        expand: typing.Optional[str] = None,
        limit: typing.Optional[int] = None,
        offset: typing.Optional[int] = None,
    ) -> types.CartPagedQueryResponse:
        params = CartQuerySchema().dump(
            {
                "where": where,
                "sort": sort,
                "expand": expand,
                "limit": limit,
                "offset": offset,
            }
        )
        return self._client._get("carts", params, schemas.CartPagedQueryResponseSchema)

    def create(self, draft: types.CartDraft) -> types.Cart:
        return self._client._post(
            "carts", {}, draft, schemas.CartUpdateSchema, schemas.CartSchema
        )

    def update(
        self, id: str, version: int, actions: List[types.CartUpdateAction]
    ) -> types.Cart:
        update_action = types.CartUpdate(version=version, actions=actions)
        return self._client._post(
            f"carts/{id}",
            {},
            update_action,
            schemas.CartUpdateSchema,
            schemas.CartSchema,
        )

    def delete(self, id: str, version: int, data_erasure: bool = False) -> types.Cart:
        params = CartDeleteSchema().dump(
            {"version": version, "data_erasure": data_erasure}
        )
        return self._client._delete(f"carts/{id}", params, schemas.CartSchema)

    def replicate(self, draft: types.ReplicaCartDraft) -> types.Cart:
        return self._client._post(
            "carts", {}, draft, schemas.CartUpdateSchema, schemas.CartSchema
        )
