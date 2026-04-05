from doc_lm.db import _Doc

from tempfile import TemporaryFile

import pytest

class Test_DocClass:
    def test_non_existent_file(self, tmp_path):
        test_file = tmp_path / "test_file.txt"
        with pytest.raises(FileNotFoundError):
            doc_obj = _Doc(test_file)
         
    def test_invalid_name_only(self, tmp_path):
        test_file = (tmp_path / "test_file.txt").touch().write_text("Content.")
        test_file.rename("123.,((_-!.jfif")
        with pytest.raises(ValueError):
            doc_obj = _Doc(test_file)



