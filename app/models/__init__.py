from .address import Address, AddressModel
from .customer import Customer, CustomerModel
from .device import Device, DeviceModel
from .event import Event, CustomerEvent, EventModel, CustomerEventModel
from .ip_address import IpAddress, IpAddressModel
from .community import CommunityModel
from .high_velocity_event import HighVelocityEvent

# @TODO: unified model registry with registry service
# add image to docker: confluentinc/cp-schema-registry:latest
# python library with faust support: https://marcosschroh.github.io/python-schema-registry-client/faust/