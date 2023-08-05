from bitcom.connection.restapi_sync_client import RestApiSyncClient
from bitcom.constant import HttpMethod


class PlaceNewOrderService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/orders"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_PRIVATE, channel, self.params)