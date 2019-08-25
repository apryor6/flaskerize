import pytest
from os import path, makedirs

from .fileio import StagedFileSystem


@pytest.fixture
def fs(tmp_path):
    schematic_path = str(tmp_path)
    schematic_files_path = path.join(schematic_path, "files/")
    makedirs(schematic_files_path)
    return StagedFileSystem(schematic_path=schematic_path, src_path=str(tmp_path))


# class TestStagedFileSystem:
def test_file_not_copied_until_commit(fs):
    outfile = path.join(fs.root, "my_file.txt")
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


# def test_existing_file_copied_to_staging_on_open(fs):
#     outfile = path.join(fs.root, "my_file.txt")
#     fs.src_fs.makedirs(path.dirname(outfile))
#     with fs.src_fs.open(outfile, "w") as fid:
#         fid.write("Some content")
#     assert fs.src_fs.exists(outfile)
#     assert not fs.stg_fs.exists(outfile)

#     with fs.open(outfile, "r") as fid:
#         r = fid.read()
#     assert fs.stg_fs.exists(outfile)
#     assert fs.src_fs.exists(outfile)


def test_dry_run_true_does_not_write_changes(tmp_path):
    schematic_files_path = path.join(tmp_path, "files/")
    makedirs(schematic_files_path)
    fs = StagedFileSystem(
        src_path=str(tmp_path), schematic_path=str(tmp_path), dry_run=True
    )
    outfile = path.join(fs.root, "my_file.txt")
    fs.stg_fs.makedirs(path.dirname(outfile))
    with fs.open(outfile, "w") as fid:
        fid.write("Some content")
    assert not fs.src_fs.exists(outfile)
    assert fs.stg_fs.exists(outfile)

    fs.commit()
    assert not fs.src_fs.exists(outfile)
    assert fs.stg_fs.exists(outfile)


# def test_dry_run_false_does_write_changes(tmp_path):
#     fs = StagedFileSystem(root=str(tmp_path), dry_run=False)
#     outfile = path.join(fs.root, "my_file.txt")
#     fs.stg_fs.makedirs(path.dirname(outfile))
#     with fs.open(outfile, "w") as fid:
#         fid.write("Some content")
#     assert not fs.src_fs.exists(outfile)
#     assert fs.stg_fs.exists(outfile)

#     fs.commit()
#     assert fs.src_fs.exists(outfile)
#     assert fs.stg_fs.exists(outfile)


def test_md5(tmp_path):
    from .fileio import md5

    outfile = path.join(tmp_path, "my_file.txt")
    with open(outfile, "w") as fid:
        fid.write("Some content")

    result = md5(lambda: open(outfile, "rb"))

    expected = "b53227da4280f0e18270f21dd77c91d0"
    assert result == expected
