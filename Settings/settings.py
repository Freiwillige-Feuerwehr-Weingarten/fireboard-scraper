from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    fb_url: str
    fb_phpsessid: str
    db_name: str
    db_host: str
    db_user: str
    db_password: str
    db_port: int
    alamos_stats_endpoint: str
    alamos_auth: str
    alamos_sender: str
    model_config = SettingsConfigDict(env_file='./.env')

def get_settings():
    return Settings()