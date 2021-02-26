from amazonspapi.spapi import SPAPI
from amazonspapi.exception import ParamsException


class Finances(SPAPI):
    """"""

    def list_financial_event_groups(
            self,
            financial_event_group_started_before=None,
            financial_event_group_started_after=None,
            max_results_per_page=100,
            next_token=None
    ):
        uri = '/finances/v0/financialEventGroups'

        if financial_event_group_started_before and financial_event_group_started_after and (
                financial_event_group_started_after > financial_event_group_started_before or (
                financial_event_group_started_before - financial_event_group_started_after).days > 180):
            raise ParamsException(
                'FinancialEventGroupStartedBefore must be later than FinancialEventGroupStartedAfter and no later than two minutes before the request was submitted')

        params = {
            'MaxResultsPerPage': max_results_per_page,
            'FinancialEventGroupStartedBefore': financial_event_group_started_before,
            'FinancialEventGroupStartedAfter': financial_event_group_started_after,

        }
        if next_token:
            params = {
                'NextToken': next_token,
            }

        return self.make_request(uri=uri, params=params, method='GET')

    def list_financial_events_by_group_id(self, max_results_per_page=100, event_group_id=None, next_token=None):
        uri = '/finances/v0/financialEventGroups/{eventGroupId}/financialEvents'.format(eventGroupId=event_group_id)
        params = {
            'MaxResultsPerPage': max_results_per_page,
            'NextToken': next_token,
        }
        return self.make_request(uri=uri, params=params, method='GET')

    def list_financial_events_by_order_id(self, order_id, max_results_per_page, next_token):
        uri = '/finances/v0/orders/{orderId}/financialEvents'.format(orderId=order_id)
        params = {
            'MaxResultsPerPage': max_results_per_page,
            'NextToken': next_token,
        }

        return self.make_request(params=params, uri=uri, method='GET')

    def list_financial_events(self, max_results_per_page, posted_after, posted_before, next_token):
        uri = '/finances/v0/financialEvents'
        params = {
            'MaxResultsPerPage': max_results_per_page,
            'PostedAfter': posted_after,
            'PostedBefore': posted_before,
            'NextToken': next_token,
        }

        return self.make_request(uri=uri, params=params, method='GET')
