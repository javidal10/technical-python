import unittest


def find_ordered_pairs(similar_ids: dict):
    pairs = set()
    for key, values in similar_ids.items():
        for value in values:
            if key < value:
                pairs.add((key, value))
            else:
                pairs.add((value, key))
    return pairs


class TestFindOrderedPairs(unittest.TestCase):
    def test_find_ordered_pairs(self):
        similar_ids = {
            123: [458, 812, 765],
            458: [123, 812, 765],
            812: [123, 458],
            765: [123, 458],
            999: [100],
            100: [999],
        }

        expected = {
            (100, 999),
            (123, 458),
            (123, 765),
            (123, 812),
            (458, 765),
            (458, 812),
        }

        self.assertEqual(find_ordered_pairs(similar_ids), expected)

    def test_find_ordered_pairs_empty_input(self):
        similar_ids = {}
        expected = set()
        self.assertEqual(find_ordered_pairs(similar_ids), expected)

    def test_find_ordered_pairs_single_element(self):
        similar_ids = {123: [456]}
        expected = set()
        self.assertEqual(find_ordered_pairs(similar_ids), expected)

    def test_find_ordered_pairs_duplicate_values(self):
        similar_ids = {123: [456, 789, 456]}
        expected = {(123, 456), (123, 789)}
        self.assertEqual(find_ordered_pairs(similar_ids), expected)

    def test_find_ordered_pairs_large_input(self):
        similar_ids = {i: [i + 1] for i in range(10**6)}
        expected = {(i, i + 1) for i in range(10**6)}
        self.assertEqual(find_ordered_pairs(similar_ids), expected)


if __name__ == "__main__":
    unittest.main()
