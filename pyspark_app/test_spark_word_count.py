import unittest

from spark_word_count import normalize_words


class NormalizeWordsTests(unittest.TestCase):
    def test_lowercases_and_preserves_accented_words(self):
        self.assertEqual(
            normalize_words("Ação, CIÊNCIA! Árvore."),
            ["ação", "ciência", "árvore"],
        )

    def test_tokenizes_more_than_twenty_distinct_words(self):
        text = " ".join(f"palavralonga{index:02d}" for index in range(30))

        words = normalize_words(text)

        self.assertEqual(len(words), 30)
        self.assertEqual(len(set(words)), 30)


if __name__ == "__main__":
    unittest.main()
