import faust
from app.config.settings import settings

# Faust app
## Autodiscovery https://faust-streaming.github.io/faust/userguide/settings.html#autodiscover
app = faust_app = faust.App(
    settings.faust_app_name,
    broker=settings.faust_broker,
    web_enabled=False,
    autodiscover=True,
    origin="app.faust",
)

# @faust_app.on_before_configured.connect
# def before_configuration(faust_app, **kwargs):
#     print(f'Faust app {settings.faust_app_name} is being configured')

# @faust_app.on_after_configured.connect
# def after_configuration(faust_app, **kwargs):
#     print(f'Faust app {settings.faust_app_name} has been configured.')

# @faust_app.on_worker_init.connect
# def on_worker_init(faust_app, **kwargs):
#     print(f'Working starting for faust app {settings.faust_app_name}')