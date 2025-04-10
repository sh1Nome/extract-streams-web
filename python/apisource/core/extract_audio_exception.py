class ExtractAudioException(Exception):
    def __init__(self, message_key: str, **kwargs):
        self.message_key = message_key
        self.kwargs = kwargs