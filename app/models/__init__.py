from app.models.address import Address, AddressModel
from app.models.customer import Customer, CustomerModel
from app.models.application import Application, ApplicationModel
from app.models.device import Device, DeviceModel
from app.models.event import Event, CustomerEvent, ApplicationEvent, EventModel, CustomerEventModel, ApplicationEventModel
from app.models.community import CommunityModel
from app.models.risk_signal import RiskSignal, SignalEnum
from app.models.graph_task import GraphTask, TaskEnum

# @TODO: unified model registry with registry service
# add image to docker: confluentinc/cp-schema-registry:latest
# python library with faust support: https://marcosschroh.github.io/python-schema-registry-client/faust/