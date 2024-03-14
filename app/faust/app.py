import faust
from app.config.settings import settings

# Faust app
# autodiscover https://faust-streaming.github.io/faust/userguide/settings.html#autodiscover
app = faust_app = faust.App(
    settings.faust_app_name,
    broker=settings.faust_broker,
    web_enabled=False,
    autodiscover=True,
    origin="app.faust",
)