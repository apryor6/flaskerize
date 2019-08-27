import pytest
from os import path, makedirs

from .fileio import StagedFileSystem


@pytest.fixture
def fs(tmp_path):
    return StagedFileSystem(src_path=str(tmp_path))


# class TestStagedFileSystem:
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


# def test_print_summary_with_updates(
#     self, colored: MagicMock, renderer: SchematicRenderer
# ):
#     renderer._files_created.append("some file I made")
#     renderer._files_modified.append("some file I modified")
#     renderer._files_deleted.append("some file I deleted")
#     renderer._directories_created.append("some directory I made/")
#     renderer.print_summary()

#     # One extra call if dry run is enabled
#     assert colored.call_count >= 4 + int(renderer.dry_run)


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

