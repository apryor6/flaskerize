from typing import Any, Callable, Optional
import os
import fs
from fs.base import FS

from _io import _IOBase


def default_src_fs_factory(path: str) -> FS:
    from fs import open_fs

    return open_fs(path)


def default_dst_fs_factory(path: str) -> FS:
    from fs import open_fs

    return open_fs(path, create=True)


class StagedFileSystem:
    """
    A filesystem that writes to an in-memory staging area and only commits the
    changes when its .commit method is invoked
    """

    def __init__(
        self,
        root: str,
        dst_root: str = None,
        srcfs_factory: Callable[..., FS] = default_src_fs_factory,
        dstfs_factory: Callable[..., FS] = default_dst_fs_factory,
        dry_run: bool = False,
    ):
        """
        
        Args:
            root (str): Root path of src file system
            srcfs_factory (Callable[..., FS], optional): Factory method for returning
                PyFileSystem object. Defaults to default_src_fs_factory.
            dstfs_factory (Callable[..., FS], optional): Factory method for returning
                PyFileSystem object. Defaults to default_src_fs_factory.
        """
        self.src_fs = srcfs_factory(root)
        if not dry_run and dst_root and not os.path.isdir(os.path.dirname(dst_root)):
            os.makedirs(os.path.dirname(dst_root))
        if not dry_run:  # during a dry run, don't even create a dst_fs
            self.dst_fs = dstfs_factory(dst_root or root)
        self.stg_fs = fs.open_fs(f"mem://")
        self.root = root
        self.dry_run = dry_run

    def commit(self) -> None:
        """Commit the in-memory staging file system to the destination"""

        if not self.dry_run:
            return fs.copy.copy_fs(self.stg_fs, self.dst_fs)

    def copy(self, src_path: str, dst_path: str = None) -> None:
        """Copy a file from src_path to dst_path in the staging file system"""

        return fs.copy.copy_file(
            self.src_fs, src_path, self.stg_fs, dst_path or src_path
        )

    def open(self, path: str, mode: str = "r") -> _IOBase:
        """
        Open a file in the staging file system, lazily copying it from the source file
        system if the file exists on the source but not yet in memory.
        """

        dirname, pathname = os.path.split(path)
        if not self.stg_fs.isdir(dirname):
            self.stg_fs.makedirs(dirname)

        if (
            not self.stg_fs.exists(path)
            and self.src_fs.exists(path)
            and "r" in mode.lower()
        ):
            # Copy from the source fs
            self.copy(path)
        return self.stg_fs.open(path, mode=mode)


def md5(fhandle_getter):
    import hashlib

    hash_md5 = hashlib.md5()
    with fhandle_getter() as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
