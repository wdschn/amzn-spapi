from amazonspapi.spapi import SPAPI
from amazonspapi.exception import ParamsException


class FbaInventory(SPAPI):
    def get_inventory_summaries(self,
                                details='false',
                                granularity_type='Marketplace',
                                granularity_id=None,
                                start_date_time=None,
                                seller_skus=None,
                                next_token=None,
                                marketplace_ids=None):
        uri = '/fba/inventory/v1/summaries'
        params = {
            'details': details,
            'granularityType': granularity_type,
            'granularityId': granularity_id,
            'startDateTime': start_date_time,
            'sellerSkus': seller_skus,
            'nextToken': next_token,
            'marketplaceIds': marketplace_ids,
        }
        return self.make_request(uri=uri, params=params)
