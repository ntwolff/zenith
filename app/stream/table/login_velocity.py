"""
Customer Login Velocity Table
"""

from datetime import timedelta
from app.stream.faust_app import faust_app
from app.config.settings import settings

login_velocity_table = faust_app.Table('login_velocity', default=int).tumbling(
    size=timedelta(minutes=settings.high_velocity_login_window_size),
    expires=timedelta(minutes=settings.high_velocity_login_window_expires),
)
