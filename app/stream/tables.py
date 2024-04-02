"""
Faust Tables
********************************
- Stateful Stream Processing
- Tumbling Windows for Computation in Agent-code
- @TODO: Explore Swap-in Scalable KV Store (e.g. RocksDB)
"""

from datetime import timedelta
from app.stream.faust_app import faust_app
from app.config.settings import settings

ip_velocity_table = faust_app.Table('ip_velocity', default=int).tumbling(
    size=timedelta(minutes=settings.high_velocity_ip_window_size),
    expires=timedelta(minutes=settings.high_velocity_ip_window_expires),
)

login_velocity_table = faust_app.Table('login_velocity', default=int).tumbling(
    size=timedelta(minutes=settings.high_velocity_login_window_size),
    expires=timedelta(minutes=settings.high_velocity_login_window_expires),
)