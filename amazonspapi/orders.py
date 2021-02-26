from .spapi import SPAPI


class OrderUtils(SPAPI):
    def get_orders(self,
                   created_after=None,
                   created_before=None,
                   last_updated_after=None,
                   last_updated_before=None,
                   order_statuses=None,
                   marketplace_ids=None,
                   fulfillment_channels=None,
                   payment_methods=None,
                   buyer_email=None,
                   sellerOrderId=None,
                   max_results_per_page=None,
                   easy_ship_shipment_statuses=None,
                   next_token=None,
                   amazon_order_ids=None
                   ):
        params = {
            'CreatedAfter': created_after,
            'CreatedBefore': created_before,
            'LastUpdatedAfter': last_updated_after,
            'LastUpdatedBefore': last_updated_before,
            'OrderStatuses': order_statuses,
            'MarketplaceIds': marketplace_ids,
            'FulfillmentChannels': fulfillment_channels,
            'PaymentMethods': payment_methods,
            'BuyerEmail': buyer_email,
            'SellerOrderId': sellerOrderId,
            'MaxResultsPerPage': max_results_per_page,
            'EasyShipShipmentStatuses': easy_ship_shipment_statuses,
            'NextToken': next_token,
            'AmazonOrderIds': amazon_order_ids,

        }
        uri = '/orders/v0/orders'
        return self.make_request(uri=uri, params=params, method='GET')

    def get_order(self, order_id):
        uri = '/orders/v0/orders/{orderId}'.format(orderId=order_id)
        return self.make_request(uri=uri, method='GET')

    def get_order_buyer_info(self, order_id):
        uri = '/orders/v0/orders/{orderId}/buyerInfo'.format(orderId=order_id)
        return self.make_request(uri=uri, method='GET')

    def get_order_address(self, order_id):
        uri = '/orders/v0/orders/{orderId}/address'.format(orderId=order_id)
        return self.make_request(uri=uri, method='GET')

    def get_order_items(self, order_id, next_token=None):
        uri = '/orders/v0/orders/{orderId}/orderItems'.format(orderId=order_id)
        params = {
            'NextToken': next_token
        }
        return self.make_request(uri=uri, params=params, method='GET')

    def get_order_items_buyer_info(self, order_id, next_token=None):
        uri = '/orders/v0/orders/{orderId}/orderItems/buyerInfo'.format(orderId=order_id)
        params = {
            'NextToken': next_token
        }
        return self.make_request(uri=uri, params=params, method='GET')
