from decouple import config


class Config:

    def __init__(self):
        self.dev = config('DEV', default=False) == True

    @property
    def API_URL(self):
        if (self.dev):
            return 'https://mila.modfy.video'
        else:
            return 'http://localhost:80'

    @property
    def SERVER_URL(self):
        if (self.dev):
            return 'https://server.modfy.video'
        else:
            return 'http://localhost:5000'
