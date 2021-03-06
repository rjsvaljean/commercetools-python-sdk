import typing
from typing import List, Optional
from uuid import UUID

from marshmallow import fields

from commercetools import schemas, types
from commercetools.services import abstract
from commercetools.typing import OptionalListStr

__all__ = ["ProductService"]


class ProductDeleteSchema(abstract.AbstractDeleteSchema):
    price_currency = fields.String(data_key="priceCurrency", required=False)
    price_country = fields.String(data_key="priceCountry", required=False)
    price_customer_group = fields.UUID(data_key="priceCustomerGroup", required=False)
    price_channel = fields.UUID(data_key="priceChannel", required=False)


class ProductQuerySchema(abstract.AbstractQuerySchema):
    price_currency = fields.String(data_key="priceCurrency", required=False)
    price_country = fields.String(data_key="priceCountry", required=False)
    price_customer_group = fields.UUID(data_key="priceCustomerGroup", required=False)
    price_channel = fields.UUID(data_key="priceChannel", required=False)


class ProductService(abstract.AbstractService):
    def get_by_id(self, id: str) -> Optional[types.Product]:
        return self._client._get(f"products/{id}", {}, schemas.ProductSchema)

    def get_by_key(self, key: str) -> types.Product:
        return self._client._get(f"products/key={key}", {}, schemas.ProductSchema)

    def query(
        self,
        where: OptionalListStr = None,
        sort: OptionalListStr = None,
        expand: typing.Optional[str] = None,
        limit: typing.Optional[int] = None,
        offset: typing.Optional[int] = None,
        price_currency: typing.Optional[str] = None,
        price_country: typing.Optional[str] = None,
        price_customer_group: typing.Optional[UUID] = None,
        price_channel: typing.Optional[UUID] = None,
    ) -> types.ProductPagedQueryResponse:
        params = ProductQuerySchema().dump(
            {
                "where": where,
                "sort": sort,
                "expand": expand,
                "limit": limit,
                "offset": offset,
                "price_currency": price_currency,
                "price_country": price_country,
                "price_customer_group": price_customer_group,
                "price_channel": price_channel,
            }
        )
        return self._client._get(
            "products", params, schemas.ProductPagedQueryResponseSchema
        )

    def create(self, draft: types.ProductDraft) -> types.Product:
        return self._client._post(
            "products", {}, draft, schemas.ProductDraftSchema, schemas.ProductSchema
        )

    def update_by_id(
        self, id: str, version: int, actions: List[types.ProductUpdateAction]
    ) -> types.Product:
        update_action = types.ProductUpdate(version=version, actions=actions)
        return self._client._post(
            f"products/{id}",
            {},
            update_action,
            schemas.ProductUpdateSchema,
            schemas.ProductSchema,
        )

    def update_by_key(
        self, key: str, version: int, actions: List[types.ProductUpdateAction]
    ) -> types.Product:
        update_action = types.ProductUpdate(version=version, actions=actions)
        return self._client._post(
            f"products/key={key}",
            {},
            update_action,
            schemas.ProductUpdateSchema,
            schemas.ProductSchema,
        )

    def delete_by_id(
        self,
        id: str,
        version: int,
        price_currency: typing.Optional[str] = None,
        price_country: typing.Optional[str] = None,
        price_customer_group: typing.Optional[UUID] = None,
        price_channel: typing.Optional[UUID] = None,
    ) -> types.Product:
        params = ProductDeleteSchema().dump(
            {
                "version": version,
                "price_currency": price_currency,
                "price_country": price_country,
                "price_customer_group": price_customer_group,
                "price_channel": price_channel,
            }
        )
        return self._client._delete(f"products/{id}", params, schemas.ProductSchema)

    def delete_by_key(
        self,
        key: str,
        version: int,
        price_currency: typing.Optional[str] = None,
        price_country: typing.Optional[str] = None,
        price_customer_group: typing.Optional[UUID] = None,
        price_channel: typing.Optional[UUID] = None,
    ) -> types.Product:
        params = ProductDeleteSchema().dump(
            {
                "version": version,
                "price_currency": price_currency,
                "price_country": price_country,
                "price_customer_group": price_customer_group,
                "price_channel": price_channel,
            }
        )
        return self._client._delete(
            f"products/key={key}", params, schemas.ProductSchema
        )

    def upload_image(
        self,
        product_id: str,
        fh: typing.BinaryIO,
        sku: str = None,
        filename: str = "img",
        staged: bool = True,
    ):
        params = {"filename": filename, "staged": staged}
        if sku:
            params["sku"] = sku

        return self._client._upload(
            f"products/{product_id}/images",
            params,
            file=fh,
            response_schema_cls=schemas.ProductSchema,
        )
