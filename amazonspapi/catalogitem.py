from .spapi import SPAPI


class CatalogItemUtils(SPAPI):

    def list_catalog_item(self, marketplace_id=None, query=None, query_context_id=None, seller_sku=None, upc=None, ean=None, isbn=None, jan=None):
        uri = '/catalog/v0/items'
        params = {
            'MarketplaceId': marketplace_id,
            'Query': query,
            'QueryContextId': query_context_id,
            'SellerSKU': seller_sku,
            'UPC': upc,
            'EAN': ean,
            'ISBN': isbn,
            'JAN': jan,
        }
        return self.make_request(uri=uri, params=params)

    def get_catalog_item(self, asin, marketplace_id):
        uri = '/catalog/v0/items/{asin}'.format(asin=asin)
        params = {
            'MarketplaceId': marketplace_id,
        }
        return self.make_request(uri=uri, params=params)

    def list_catalog_categories(self, marketplace_id, asin=None, seller_sku=None):
        uri = '/catalog/v0/categories'
        params = {
            'MarketplaceId': marketplace_id,
            'ASIN': asin,
            'SellerSKU': seller_sku,
        }

        return self.make_request(uri=uri, params=params)
