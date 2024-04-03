import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field

class Neo4jSettings(BaseModel):
    neo4j_uri: str = Field(default='bolt://neo4j:7687')
    neo4j_user: str = Field(default='neo4j')
    neo4j_password: str = Field(default='password')

    # model_config = SettingsConfigDict(
    #     env_prefix = "NEO4J_"
    # )

class KafkaSettings(BaseModel):
    kafka_topic_partitions: int = Field(default=4)
    kafka_topic_replication_factor: int = Field(default=1)
    kafka_schema_registry_url: str = Field(default='http://kafka:8081')

    # model_config = SettingsConfigDict(
    #     env_prefix = "KAFKA_"
    # )

class FastApiSettings(BaseModel):
    fastapi_host: str = Field(default='0.0.0.0')
    fastapi_port: int = Field(default=8000)

    # model_config = SettingsConfigDict(
    #     env_prefix = "FASTAPI_"
    # )

class FaustSettings(BaseModel):
    faust_app_name: str = Field(default='zenith')
    faust_broker: str = Field(default='kafka://kafka:9092')

    # model_config = SettingsConfigDict(
    #     env_prefix = "FAUST_"
    # )

class RedisSettings(BaseModel):
    redis_host: str = Field(default='localhost')
    redis_port: int = Field(default=6379)
    redis_db: int = Field(default=0)
    redis_password: str = Field(default='')

    # model_config = SettingsConfigDict(
    #     env_prefix = "REDIS_"
    # )

class MongoDBSettings(BaseModel):
    mongodb_uri: str = Field(default='mongodb://localhost:27017')
    mongodb_database: str = Field(default='zenith')

    # model_config = SettingsConfigDict(
    #     env_prefix = "MONGODB_"
    # )

class GoogleMapsSettings(BaseModel):
    google_maps_api_key: str = Field(default='')
    google_maps_enabled: bool = Field(default=False)

    # model_config = SettingsConfigDict(
    #     env_prefix = "GOOGLE_MAPS_",
    #     extra = 'allow'
    # )

class Settings(BaseSettings):
    neo4j: Neo4jSettings
    kafka: KafkaSettings
    fastapi: FastApiSettings
    faust: FaustSettings
    redis: RedisSettings
    mongodb: MongoDBSettings
    google_maps: GoogleMapsSettings

    # Feature Flags
    fake_data_generation_enabled: bool = Field(default=False)
    ml_detection_enabled: bool = Field(default=False)

    # Streamling Tables
    high_velocity_ip_window_size: int = Field(default=5)
    high_velocity_ip_window_expires: int = Field(default=60)
    high_velocity_login_window_size: int = Field(default=5)
    high_velocity_login_window_expires: int = Field(default=60)

    model_config = SettingsConfigDict(
        env_file =('.env'),
        env_file_encoding =('utf-8')
    )

settings = Settings(
    neo4j=Neo4jSettings(), 
    kafka=KafkaSettings(), 
    fastapi=FastApiSettings(), 
    faust=FaustSettings(), 
    redis=RedisSettings(), 
    mongodb=MongoDBSettings(), 
    google_maps=GoogleMapsSettings()
)
