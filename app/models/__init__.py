from .address import Address
from .customer import Customer
from .device import Device
from .event import Event, CustomerEvent
from .ip_address import IpAddress

# @TODO: unified model registry with registry service
# add image to docker: confluentinc/cp-schema-registry:latest
# python library with faust support: https://marcosschroh.github.io/python-schema-registry-client/faust/