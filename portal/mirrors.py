# To create wrapper classes for data received in API calls.

from abc import ABCMeta, abstractmethod


class ModelMirror(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self):
        pass


class BotUser(ModelMirror):

    def __init__(self, first_name, last_name, username, dob, gender, fb_id, on_portal=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.dob = dob
        self.gender = gender
        self.fb_id = fb_id
        self.on_portal = on_portal

    def save(self):
        pass


# Add other ModelMirrors