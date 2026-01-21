from helpers import Settings
from domain.providers import WhisperProvider

from logging import getLogger

logger = getLogger(__name__)

class AudioService:
    def __init__(self):
        self.settings = Settings()

        self.STT_provider = None
        self.TTS_provider = None
    
    @classmethod
    def initialize_service(cls):
        self = cls()
        self.STT_provider = WhisperProvider()
        SST_provider_is_created = self.STT_provider.set_whisper_model(
                                        self.settings.WHISPER_MODEL_SIZE,
                                        self.settings.WHISPER_COMPUTE_TYPE,
                                        self.settings.WHISPER_BEAM_SIZE,
                                          )
        
        if not SST_provider_is_created:
            logger.error("❌ SST provider Audio service can't be initialized")
            return False
        
        # TODO: add TTS provider here 


        return self
    def transcribe(self, audio_file):
        segments, info = self.STT_provider.transcribe(audio_file)

        return segments, info
    
    def close(self):
        self.STT_provider = None
        self.TTS_provider = None
        

        
