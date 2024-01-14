#!/usr/bin/python3
"""Defines unittests for models/user.py.
Unittest classes:
    TestUserInstantiation
    TestUserSave
    TestUserToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUserInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the User class."""

    def test_no_args_instantiates(self):
        user = User()
        self.assertIsInstance(user, User)

    def test_new_instance_stored_in_objects(self):
        user = User()
        self.assertIn(user, models.storage.all().values())

    def test_id_is_public_str(self):
        user = User()
        self.assertIsInstance(user.id, str)

    def test_created_at_is_public_datetime(self):
        user = User()
        self.assertIsInstance(user.created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        user = User()
        self.assertIsInstance(user.updated_at, datetime)

    def test_email_is_public_str(self):
        user = User()
        self.assertIsInstance(user.email, str)

    def test_password_is_public_str(self):
        user = User()
        self.assertIsInstance(user.password, str)

    def test_first_name_is_public_str(self):
        user = User()
        self.assertIsInstance(user.first_name, str)

    def test_last_name_is_public_str(self):
        user = User()
        self.assertIsInstance(user.last_name, str)

    def test_two_users_unique_ids(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_two_users_different_created_at(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_two_users_different_updated_at(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_str_representation(self):
        user = User()
        user.id = "123456"
        user.created_at = datetime.now()
        user.updated_at = datetime.now()
        expected_str = (
            "[User] (123456) {'id': '123456', 'created_at': <datetime>, "
            "'updated_at': <datetime>}"
        )
        self.assertEqual(str(user), expected_str)

    def test_args_unused(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.now()
        user = User(id="345", created_at=dt, updated_at=dt)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, dt)
        self.assertEqual(user.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserSave(unittest.TestCase):
    """Unittests for testing save method of the User class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except FileNotFoundError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmp", "file.json")
        except FileNotFoundError:
            pass

    def test_one_save(self):
        user = User()
        first_updated_at = user.updated_at
        user.save()
        self.assertLess(first_updated_at, user.updated_at)

    def test_two_saves(self):
        user = User()
        first_updated_at = user.updated_at
        user.save()
        second_updated_at = user.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        user.save()
        self.assertLess(second_updated_at, user.updated_at)

    def test_save_with_arg(self):
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    def test_save_updates_file(self):
        user = User()
        user.save()
        user_id = "User." + user.id
        with open("file.json", "r") as f:
            self.assertIn(user_id, f.read())


class TestUserToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def test_to_dict_type(self):
        user = User()
        user_dict = user.to_dict()
        self.assertIsInstance(user_dict, dict)

    def test_to_dict_contains_correct_keys(self):
        user = User()
        user_dict = user.to_dict()
        self.assertIn("id", user_dict)
        self.assertIn("created_at", user_dict)
        self.assertIn("updated_at", user_dict)
        self.assertIn("__class__", user_dict)

    def test_to_dict_contains_added_attributes(self):
        user = User()
        user.middle_name = "Holberton"
        user.my_number = 98
        self.assertEqual("Holberton", user.middle_name)
        user_dict = user.to_dict()
        self.assertIn("my_number", user_dict)

    def test_to_dict_datetime_attributes_are_strs(self):
        user = User()
        user_dict = user.to_dict()
        self.assertIsInstance(user_dict["id"], str)
        self.assertIsInstance(user_dict["created_at"], str)
        self.assertIsInstance(user_dict["updated_at"], str)

    def test_to_dict_output(self):
        user = User()
        user.id = "123456"
        dt = datetime.now()
        user.created_at = dt
        user.updated_at = dt
        user_dict = user.to_dict()
        expected_dict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(user_dict, expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)

    def test_to_dict_with_arg(self):
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)


if _name_ == "_main_":
    unittest.main()
