import unittest
from pathlib import Path
import tempfile

from summarizer_agent import check_file_path, MAX_WORDS

class TestCheckFilePath(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_non_txt_file_extension_rejected(self):
        pdf_file = self.temp_path / "document.pdf"
        pdf_file.write_text("Some text content")
        result = check_file_path(pdf_file)
        
        self.assertIsNotNone(result)
        self.assertIn("is not a .txt file", result)

    def test_file_without_extension_rejected(self):
        no_ext_file = self.temp_path / "document"
        no_ext_file.write_text("Some text content")
        result = check_file_path(no_ext_file)
        
        self.assertIsNotNone(result)
        self.assertIn("is not a .txt file", result)

    def test_valid_txt_file_passes(self):
        txt_file = self.temp_path / "document.txt"
        txt_file.write_text("This is a valid text file with a few words.")
        result = check_file_path(txt_file)
        
        self.assertIsNone(result)

    def test_non_existent_file_handled(self):
        missing_file = self.temp_path / "missing.txt"
        result = check_file_path(missing_file)
        
        self.assertIsNotNone(result)
        self.assertIn("does not exist", result)

    def test_empty_txt_file_rejected(self):
        empty_file = self.temp_path / "empty.txt"
        empty_file.write_text("   \n  ")
        result = check_file_path(empty_file)
        
        self.assertIsNotNone(result)
        self.assertIn("is empty", result)

    def test_exceeds_max_words_limit(self):
        large_file = self.temp_path / "large.txt"
        large_file.write_text("word " * 801)
        result = check_file_path(large_file)
        
        self.assertIsNotNone(result)
        self.assertIn("exceeds the maximum limit", result)

if __name__ == "__main__":
    unittest.main()