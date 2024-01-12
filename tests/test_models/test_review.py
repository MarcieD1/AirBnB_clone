#!/usr/bin/python3
"""Defines unittests for models/review.py.
Unittest classes:
    TestReviewInstantiation
    TestReviewSave
    TestReviewToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReviewInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_no_args_instantiates(self):
        review = Review()
        self.assertIsInstance(review, Review)

    def test_new_instance_stored_in_objects(self):
        review = Review()
        self.assertIn(review, models.storage.all().values())

    def test_id_is_public_str(self):
        review = Review()
        self.assertIsInstance(review.id, str)

    def test_created_at_is_public_datetime(self):
        review = Review()
        self.assertIsInstance(review.created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        review = Review()
        self.assertIsInstance(review.updated_at, datetime)

    def test_place_id_is_public_class_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(review))
        self.assertNotIn("place_id", review.__dict__)

    def test_user_id_is_public_class_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(review))
        self.assertNotIn("user_id", review.__dict__)

    def test_text_is_public_class_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(review))
        self.assertNotIn("text", review.__dict__)

    def test_two_reviews_unique_ids(self):
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)

    def test_two_reviews_different_created_at(self):
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.created_at, review2.created_at)

    def test_two_reviews_different_updated_at(self):
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.updated_at, review2.updated_at)

    def test_str_representation(self):
        review = Review()
        review.id = "123456"
        dt = datetime.today()
        review.created_at = dt
        review.updated_at = dt
        expected_str = (
            "[Review] (123456) {'id': '123456', 'created_at': <datetime>, "
            "'updated_at': <datetime>}"
        )
        self.assertEqual(str(review), expected_str)

    def test_args_unused(self):
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        review = Review(id="345", created_at=dt, updated_at=dt)
        self.assertEqual(review.id, "345")
        self.assertEqual(review.created_at, dt)
        self.assertEqual(review.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReviewSave(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

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
        review = Review()
        first_updated_at = review.updated_at
        review.save()
        self.assertLess(first_updated_at, review.updated_at)

    def test_two_saves(self):
        review = Review()
        first_updated_at = review.updated_at
        review.save()
        second_updated_at = review.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        review.save()
        self.assertLess(second_updated_at, review.updated_at)

    def test_save_with_arg(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.save(None)

    def test_save_updates_file(self):
        review = Review()
        review.save()
        review_id = "Review." + review.id
        with open("file.json", "r") as f:
            self.assertIn(review_id, f.read())


class TestReviewToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def test_to_dict_type(self):
        review = Review()
        review_dict = review.to_dict()
        self.assertIsInstance(review_dict, dict)

    def test_to_dict_contains_correct_keys(self):
        review = Review()
        review_dict = review.to_dict()
        self.assertIn("id", review_dict)
        self.assertIn("created_at", review_dict)
        self.assertIn("updated_at", review_dict)
        self.assertIn("__class__", review_dict)

    def test_to_dict_contains_added_attributes(self):
        review = Review()
        review.middle_name = "Holberton"
        review.my_number = 98
        self.assertEqual("Holberton", review.middle_name)
        review_dict = review.to_dict()
        self.assertIn("my_number", review_dict)

    def test_to_dict_datetime_attributes_are_strs(self):
        review = Review()
        review_dict = review.to_dict()
        self.assertIsInstance(review_dict["id"], str)
        self.assertIsInstance(review_dict["created_at"], str)
        self.assertIsInstance(review_dict["updated_at"], str)

    def test_to_dict_output(self):
        review = Review()
        review.id = "123456"
        dt = datetime.today()
        review.created_at = dt
        review.updated_at = dt
        review_dict = review.to_dict()
        expected_dict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(review_dict, expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        review = Review()
        self.assertNotEqual(rv.to_dict(), rv.__dict__)

    def test_to_dict_with_arg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.to_dict(None)


if __name__ == "__main__":
    unittest.main()
