#!/usr/bin/python3
"""This module defines the Amenity class"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Class for managing Amenity objects"""

    def __init__(self, *args, **kwargs):
        """Initializes Amenity attributes"""
        super().__init__(*args, **kwargs)
        self.name = ""

    def __str__(self):
        """Returns a string representation of Amenity"""
        return "[Amenity] ({}) {}".format(self.id, self.__dict__)

    def to_dict(self):
        """Returns a dictionary representation of Amenity"""
        amenity_dict = super().to_dict()
        amenity_dict["name"] = self.name
        return amenity_dict
