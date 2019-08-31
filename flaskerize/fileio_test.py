from unittest.mock import patch, MagicMock
import pytest
from os import path, makedirs

from .fileio import StagedFileSystem


@pytest.fixture
def fs(tmp_path):
    return StagedFileSystem(src_path=str(tmp_path))


def test_file_not_copied_until_commit(fs):
    outfile = path.join(fs.src_path, "my_file.txt")
    assert not fs.src_fs.exists(outfile)
    assert not fs.stg_fs.exists(outfile)
    assert not fs.src_fs.exists(outfile)

    fs.stg_fs.makedirs(path.dirname(outfile))
    with fs.open(outfile, "w") as fid:
        fid.write("Some content")
    assert not fs.src_fs.exists(outfile)
    assert fs.stg_fs.exists(outfile)

    fs.commit()
    assert fs.stg_fs.exists(outfile)
    assert fs.src_fs.exists(outfile)


def test_dry_run_true_does_not_write_changes(tmp_path):
    schematic_files_path = path.join(tmp_path, "files/")
    makedirs(schematic_files_path)
    fs = StagedFileSystem(src_path=str(tmp_path), dry_run=True)
    outfile = path.join(str(tmp_path), "my_file.txt")
    fs.stg_fs.makedirs(path.dirname(outfile))
    with fs.open(outfile, "w") as fid:
        fid.write("Some content")
    assert not fs.src_fs.exists(outfile)
    assert fs.stg_fs.exists(outfile)

    fs.commit()
    assert not fs.src_fs.exists(outfile)
    assert fs.stg_fs.exists(outfile)


def test_md5(tmp_path):
    from .fileio import md5

    outfile = path.join(tmp_path, "my_file.txt")
    with open(outfile, "w") as fid:
        fid.write("Some content")

    result = md5(lambda: open(outfile, "rb"))

    expected = "b53227da4280f0e18270f21dd77c91d0"
    assert result == expected


def test_makedirs(tmp_path, fs):
    mock = MagicMock()
    fs.render_fs.makedirs = mock
    fs.makedirs(tmp_path)
    mock.assert_called_with(tmp_path)


def test_exists(tmp_path, fs):
    mock = MagicMock()
    fs.render_fs.exists = mock
    fs.exists(tmp_path)
    mock.assert_called_with(tmp_path)


def test_isdir(tmp_path, fs):
    mock = MagicMock()
    fs.render_fs.isdir = mock
    fs.isdir(tmp_path)
    mock.assert_called_with(tmp_path)


def test_delete(tmp_path, fs):
    dirname = path.join(tmp_path, "my/dir")
    fs.stg_fs.makedirs(dirname)
    with pytest.raises(NotImplementedError):
        fs.delete(dirname)

