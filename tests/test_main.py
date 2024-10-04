import unittest
from main import similarity_score, score_match, find_duplicates


class SimilarityScoreTest(unittest.TestCase):
    def test_both_strings_empty(self):
        self.assertEqual(similarity_score("", ""), 0.0)

    def test_one_string_empty(self):
        self.assertEqual(similarity_score("test", ""), 0.0)
        self.assertEqual(similarity_score("", "test"), 0.0)

    def test_identical_strings(self):
        self.assertEqual(similarity_score("test", "test"), 1.0)

    def test_completely_different_strings(self):
        self.assertEqual(similarity_score("abc", "xyz"), 0.0)

    def test_partially_similar_strings(self):
        self.assertGreater(similarity_score("abc", "abx"), 0.0)
        self.assertLess(similarity_score("abc", "abx"), 1.0)


class ScoreMatchTest(unittest.TestCase):
    def setUp(self):
        self.contact_a = {
            "email": "test@example.com",
            "name": "Diego",
            "name1": "Sadrinas",
            "address": "123 Hello World St",
            "postalZip": "12345",
            "contactID": "1",
        }
        self.contact_b = {
            "email": "test@example.com",
            "name": "Diego",
            "name1": "Sadrinas",
            "address": "123 Hello World St",
            "postalZip": "12345",
            "contactID": "2",
        }

    def test_all_fields_match(self):
        self.assertEqual(score_match(self.contact_a, self.contact_b), "High")

    def test_partial_match(self):
        self.contact_b["email"] = "test2@example.com"
        self.contact_b["name"] = "Diegol"
        self.contact_b["name1"] = "Sadri"
        self.contact_b["address"] = "124 Hello World St"
        self.contact_b["postalZip"] = "12346"
        self.assertEqual(score_match(self.contact_a, self.contact_b), "Medium")

    def test_no_fields_match(self):
        self.contact_b["email"] = "different@example.com"
        self.contact_b["name"] = "Santiago"
        self.contact_b["name1"] = "Sadri"
        self.contact_b["address"] = "456 Elm St"
        self.contact_b["postalZip"] = "67890"
        self.assertEqual(score_match(self.contact_a, self.contact_b), "Low")

    def test_only_email_matches(self):
        self.contact_b["name"] = "Sofia"
        self.contact_b["name1"] = "Smith"
        self.contact_b["address"] = "456 Elm St"
        self.contact_b["postalZip"] = "67890"
        self.assertEqual(score_match(self.contact_a, self.contact_b), "Medium")

    def test_only_postalZip_matches(self):
        self.contact_b["email"] = "different@example.com"
        self.contact_b["name"] = "Elio"
        self.contact_b["name1"] = "Smith"
        self.contact_b["address"] = "456 Elm St"
        self.assertEqual(score_match(self.contact_a, self.contact_b), "Low")


class FindDuplicatesTest(unittest.TestCase):
    def setUp(self):
        self.contact_a = {
            "contactID": "1",
            "email": "test@example.com",
            "name": "John",
            "name1": "Doe",
            "address": "123 Main St",
            "postalZip": "12345",
        }
        self.contact_b = {
            "contactID": "2",
            "email": "test@example.com",
            "name": "John",
            "name1": "Doe",
            "address": "123 Main St",
            "postalZip": "12345",
        }
        self.contact_c = {
            "contactID": "3",
            "email": "different@example.com",
            "name": "Jane",
            "name1": "Smith",
            "address": "456 Elm St",
            "postalZip": "67890",
        }

    def test_empty_contacts(self):
        self.assertEqual(find_duplicates([]), [])

    def test_single_contact(self):
        self.assertEqual(find_duplicates([self.contact_a]), [])

    def test_two_identical_contacts(self):
        duplicates = find_duplicates([self.contact_a, self.contact_b])
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0]["ContactID Source"], "1")
        self.assertEqual(duplicates[0]["ContactID Match"], "2")
        self.assertEqual(duplicates[0]["Accuracy"], "High")

    def test_two_different_contacts(self):
        duplicates = find_duplicates([self.contact_a, self.contact_c])
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0]["ContactID Source"], "1")
        self.assertEqual(duplicates[0]["ContactID Match"], "3")
        self.assertEqual(duplicates[0]["Accuracy"], "Low")

    def test_multiple_contacts_with_duplicates(self):
        duplicates = find_duplicates([self.contact_a, self.contact_b, self.contact_c])
        self.assertEqual(len(duplicates), 3)
        self.assertEqual(duplicates[0]["ContactID Source"], "1")
        self.assertEqual(duplicates[0]["ContactID Match"], "2")
        self.assertEqual(duplicates[0]["Accuracy"], "High")
        self.assertEqual(duplicates[1]["ContactID Source"], "1")
        self.assertEqual(duplicates[1]["ContactID Match"], "3")
        self.assertEqual(duplicates[1]["Accuracy"], "Low")
        self.assertEqual(duplicates[2]["ContactID Source"], "2")
        self.assertEqual(duplicates[2]["ContactID Match"], "3")
        self.assertEqual(duplicates[2]["Accuracy"], "Low")


if __name__ == "__main__":
    unittest.main()
