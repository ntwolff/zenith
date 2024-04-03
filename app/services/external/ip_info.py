import aiohttp
from unittest.mock import Mock
from .base import ExternalService
from app.models import IpAddress
from app.models.external import IpInfo

class IpInfoService(ExternalService):
    def __init__(self, mock_enabled=False):
            self.mock_enabled = mock_enabled
            if mock_enabled:
                self.mock = Mock()
                self.mock.enrich.return_value = MOCK_IP_ADDRESS

    async def enrich(self, ip_address: IpAddress) -> IpInfo:
        if self.mock_enabled:
            return self.mock.enrich(ip_address)

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://ipinfo.io/{ip_address.ipv4}/json') as response:
                data = await response.json()
                ip_info = IpInfo(**data)
                ip_address.city = ip_info.city
                ip_address.region = ip_info.region
                ip_address.country = ip_info.country
                ip_address.location = ip_info.loc
                ip_address.organization = ip_info.org
                ip_address.postal_code = ip_info.postal
                ip_address.timezone = ip_info.timezone
        return ip_address


# --------------
# Mock Data
# --------------

MOCK_IP_ADDRESS = IpInfo(
                    ip='192.168.0.1',
                    city='Mock City',
                    region='Mock Region',
                    country='Mock Country',
                    location='12.3456,-78.9012',
                    organization='Mock Organization',
                    postal_code='12345',
                    timezone='Mock/Timezone'
                )
