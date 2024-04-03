from unittest.mock import Mock
from googlemaps import Client
from app.services.external.base import ExternalService
from app.models.customer import Address
from app.config.settings import settings

class GoogleMapsService(ExternalService):
    def __init__(self):
        self.enabled = settings.google_maps.google_maps_enabled
        if not self.enabled:
            self.mock = Mock()
            self.mock.enrich.return_value = MOCK_RESULT
        else:
            self.client = Client(key=settings.google_maps.google_maps_api_key)

    def enrich(self, address: Address) -> Address:
        if not self.enabled:
            return address
            #@TODO - mock_result = self.mock.enrich(address)

        result = call_api(address)
        assert result is not None
        valid_address = self.valid_result(result)

        if valid_address:
            address.is_valid = True

            # Validated Geolocation
            geocode = result['result']['geocode']
            address.latitude = geocode['location']['latitude']
            address.longitude = geocode['location']['longitude']
        else:
            address.is_valid = False

        return address


    def valid_result(self, gmaps_result) -> bool:
        verdict = gmaps_result['result']['verdict']
        is_valid = None

        if 'addressComplete' not in verdict or verdict['validationGranularity'] == 'OTHER':
            is_valid = False
        elif verdict['addressComplete'] and (
            'hasUnconfirmedComponents' in verdict
            or 'hasInferredComponents' in verdict
            or 'hasReplacedComponents' in verdict):
            is_valid = True  # @TODO: Additional confirmation
        elif verdict['addressComplete'] and verdict['validationGranularity'] == 'APPROXIMATE':
            is_valid = True
        else:
            is_valid = False  # Unknown scenario

        return is_valid


#Google Maps Address Verification API
def call_api(self, address: Address) -> dict:
    address_string = f"{address.street}, {address.city}, {address.state} {address.zip}"
    return self.client.addressvalidation([address_string], regionCode="US")


# --------------
# Mock Data
# --------------

MOCK_RESULT = {
    'responseId': 'mock_response_id',
    'result': {
        'verdict': {
            'addressComplete': True,
            'validationGranularity': 'APPROXIMATE',
        },
        'address': {
            'addressComponents': [
                {'componentType': 'street_number', 'componentName': {'text': '123'}},
                {'componentType': 'route', 'componentName': {'text': 'Main St'}},
                {'componentType': 'locality', 'componentName': {'text': 'Springfield'}},
                {'componentType': 'administrative_area_level_1', 'componentName': {'text': 'IL'}},
                {'componentType': 'postal_code', 'componentName': {'text': '62701'}},
            ],
        },
        'geocode': {
            'location': {
                'latitude': 39.7817,
                'longitude': -89.6500,
            },
        },
    },
}
