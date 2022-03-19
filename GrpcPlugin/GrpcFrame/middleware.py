from abc import ABC, abstractmethod



class BaseMiddleware(ABC):
    def __init__(self):
        self.request=None
        self.response=None

    @abstractmethod
    def before_function(self):
        ...

    @abstractmethod
    def after_function(self):
        ...