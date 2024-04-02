"""
Address Service
"""
import logging
from googlemaps import Client
from app.services._base import BaseService
from app.models.address import Address
from app.config.settings import settings

class AddressService(BaseService):
    def validate_address(self, address: Address) -> Address:
        """
        Validate address using Google Maps API
        """

        if not settings.google_maps_enabled:
            return address

        gmaps = Client(key=settings.google_maps_api_key)

        # Construct the address string
        address_string = f"{address.street}, {address.city}, {address.state} {address.zip}"

        # Validate the address using the Google Maps Address Validation API
        result = gmaps.addressvalidation([address_string], regionCode="US")

        # Store link to the validation response
        address.validation_id = result['responseId']

        if result and self.is_valid_address(result):
            # Extract the relevant information from the validation response
            validated_address = result['result']['address']
            address_components = validated_address['addressComponents']
            geocode = result['result']['geocode']

            # Update the address model with the validated information
            address.is_valid = True
            address.latitude = geocode['location']['latitude']
            address.longitude = geocode['location']['longitude']

            # Update the address fields based on the address components
            for component in address_components:
                component_type = component['componentType']
                component_name = component['componentName']['text']

                if component_type == 'street_number':
                    address.street = f"{component_name} {address.street}"
                elif component_type == 'route':
                    address.street = f"{address.street} {component_name}"
                elif component_type == 'locality':
                    address.city = component_name
                elif component_type == 'administrative_area_level_1':
                    address.state = component_name
                elif component_type == 'postal_code':
                    address.zip = component_name

            logging.info(f"Address validated: {address}")
        else:
            address.is_valid = False
            logging.info(f"Address not validated: {address}")

        return address

    def is_valid_address(self, gmaps_result) -> bool:
        """
        Google Maps Response Validation Logic
        *************************************
        @TODO: Corner Cases
        """
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
