from flask import request
from flask_restful import Resource
from api.utils import validates_post_schema, AdminResource
from models.pricing import PricingRules
from api.utils import validates_post_schema
from api.schemas.admins import PricingSchema


class Pricing(Resource):
    def get(self):
        rule = PricingRules.get_current_rule()
        ret = rule.raw_data if rule is not None else {}
        return ret, 200

    @validates_post_schema(PricingSchema)
    def put(self, post_data):
        PricingRules.update_rule(data=post_data)
        return 'Ok', 200