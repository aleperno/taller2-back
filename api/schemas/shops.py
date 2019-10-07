from marshmallow import (
    fields,
    Schema,
    validates_schema,
    ValidationError,
    )
from api.validators import shop_exists, product_exists, product_belongs_shop


class NewShopSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    address = fields.Str(required=True)
    location = fields.Str(required=True)
    category = fields.Str(required=True)


class NewProductSchema(Schema):
    shop_id = fields.Int(required=True, validate=shop_exists)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    category = fields.Str(required=True)
    price = fields.Float(required=True)


class ItemSchema(Schema):
    id = fields.Int(required=True, validate=product_exists)
    quantity = fields.Int(required=True)


class OrderSchema(Schema):
    user_id = fields.Int(required=True)
    shop_id = fields.Int(required=True, validate=shop_exists)
    products = fields.List(fields.Nested(ItemSchema), required=True)
    user_location = fields.Str(required=True)

    @validates_schema
    def validate_products(self, data, **kw):
        products = data['products']
        shop_id = data['shop_id']
        if not products:
            raise ValidationError('Products cannot be empty', field_name='products')
        for product in products:
            product_id = product['id']
            if not product_belongs_shop(product_id, shop_id):
                raise ValidationError(f'Product {product_id} does not belong to shop {shop_id}', field_name='products')

