from pydantic import BaseSettings

class Settings(BaseSettings):
    CRED_File: str
    MIN_LOSS: int
    EPOCHS: int
    BATCH_SIZE:int
    ESTIMTED_WORK_DAY: int
    NOVEL_QUEUE: str
    HOST: str
    REVIEW_QUEUE: str
    
    
    
    
    class Config:
        env_file = "..env"
    
    
settings = Settings()   