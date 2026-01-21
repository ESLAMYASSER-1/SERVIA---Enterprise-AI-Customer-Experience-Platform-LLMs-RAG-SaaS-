from helpers import Settings
from logging import getLogger
import torch
from pathlib import Path

from faster_whisper import WhisperModel

logger = getLogger(__name__)


class WhisperProvider:
    def __init__(self):
        self.settings = Settings()
        self.model_size = None
        self.compute_type = None
        self.beam_size = None
        self.model = None


    def set_whisper_model(self, model_size, compute_type, beam_size):

        self.model_size = model_size
        self.compute_type = compute_type
        self.beam_size = beam_size
    
        if not self.model_size:
            logger.error("❌ There is no whisper model size in your env arguments")
            return False 
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = WhisperModel(self.model_size,
                                  device=device,
                                  compute_type = self.compute_type,
                                  download_root = Path(self.settings.ASSETS_FOLDER)/self.settings.STT_MODELS_FOLDER)
        
        if not self.model:
            return False
        else:
            return True
    
    def transcribe(self, audio_file):
        segments_generator, info = self.model.transcribe(audio_file, beam_size = self.beam_size)

        if not segments_generator :
            return False
        segments = []
        for segment in segments_generator:
            segments.append(segment)

        
        return segments, info
        
