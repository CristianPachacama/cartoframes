from abc import ABCMeta, abstractmethod


class BaseClient():
    __metaclass__ = ABCMeta

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def upload(self):
        pass

    @abstractmethod
    def execute_query(self):
        pass

    @abstractmethod
    def execute_long_running_query(self):
        pass