#!/usr/bin/python3
"""This module defines the State class"""
from models.base_model import BaseModel

class State(BaseModel):
    """Class for managing state objects"""

    def _init_(self, *args, **kwargs):
        """Initializes State instance"""
        super()._init_(*args, **kwargs)
        self.name = ""

    def _str_(self):
        """Returns a string representation of the State instance"""
        return "[State] ({}) {}".format(self.id, self._dict_)
