import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application settings
    fake_data_generation_enabled: bool = os.environ.get('FAKE_DATA_GENERATION_ENABLED', 'false').lower() == 'true'

    # Kafka settings
    kafka_topic_partitions: int = int(os.environ.get('KAFKA_TOPIC_PARTITIONS', '4'))

    # Neo4j settings
    neo4j_uri: str = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user: str = os.environ.get('NEO4J_USER', 'neo4j')
    neo4j_password: str = os.environ.get('NEO4J_PASSWORD', 'password')

    # FastAPI settings
    fastapi_host: str = os.environ.get('FASTAPI_HOST', '0.0.0.0')
    fastapi_port: int = int(os.environ.get('FASTAPI_PORT', '8000'))

    # Faust settings
    faust_app_name: str = os.environ.get('FAUST_APP_NAME', 'fraud-detection-system')
    faust_broker: str = os.environ.get('FAUST_BROKER', 'kafka://fast-data-dev:9092')

    # Processor settings
    high_velocity_ip_window_size: int = int(os.environ.get('HIGH_VELOCITY_IP_WINDOW_SIZE', '5'))
    high_velocity_ip_window_expires: int = int(os.environ.get('HIGH_VELOCITY_IP_WINDOW_EXPIRES', '60'))
    high_velocity_login_window_size: int = int(os.environ.get('HIGH_VELOCITY_LOGIN_WINDOW_SIZE', '5'))
    high_velocity_login_window_expires: int = int(os.environ.get('HIGH_VELOCITY_LOGIN_WINDOW_EXPIRES', '60'))

    # Google Maps settings
    google_maps_api_key: str = os.environ.get('GOOGLE_MAPS_API_KEY', '')
    google_maps_enabled: bool = os.environ.get('GOOGLE_MAPS_ENABLED', 'false').lower() == 'true'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()