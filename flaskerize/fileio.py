from typing import Any, Callable, Optional
import os
import fs
from fs.base import FS

from _io import _IOBase


def default_nocreate_fs_factory(path: str) -> FS:
    from fs import open_fs

    return open_fs(path)


def default_fs_factory(path: str) -> FS:
    from fs import open_fs

    return open_fs(path, create=True)


class StagedFileSystem:
    """
    A filesystem that writes to an in-memory staging area and only commits the
    changes when its .commit method is invoked
    """

    def __init__(
        self,
        schematic_path: str,
        src_path: str = None,
        sch_fs_factory: Callable[..., FS] = default_nocreate_fs_factory,
        src_fs_factory: Callable[..., FS] = default_fs_factory,
        dry_run: bool = False,
    ):
        """
        
        Args:
            schematic_path (str): Root path of schematic
            sch_fs_factory (Callable[..., FS], optional): Factory method for returning
                PyFileSystem object. Defaults to default_nocreate_fs_factory.
            src_fs_factory (Callable[..., FS], optional): Factory method for returning
                PyFileSystem object. Defaults to default_nocreate_fs_factory.
        """
        schematic_files_path = os.path.join(schematic_path, "files/")
        self.sch_fs = sch_fs_factory(schematic_files_path)
        if not dry_run and src_path and not os.path.isdir(os.path.dirname(src_path)):
            os.makedirs(os.path.dirname(src_path))
        # if not dry_run:  # during a dry run, don't even create a src_fs
        # self.src_fs = src_fs_factory(src_path or root)
        self.src_fs = src_fs_factory(src_path or schematic_path)
        self.stg_fs = fs.open_fs(f"mem://")
        self.root = schematic_path
        self.dry_run = dry_run

    def commit(self) -> None:
        """Commit the in-memory staging file system to the destination"""

        if not self.dry_run:
            return fs.copy.copy_fs(self.stg_fs, self.src_fs)

    def copy_from_sch(self, src_path: str, dst_path: str = None) -> None:
        """Copy a file from src_path to dst_path in the staging file system"""

        dst_path = dst_path or src_path
        dst_dir = os.path.dirname(dst_path)
        if not self.stg_fs.exists(dst_dir):
            self.stg_fs.makedirs(dst_dir)
        return fs.copy.copy_file(
            self.sch_fs, src_path, self.stg_fs, dst_path or src_path
        )

    def copy_from_src(self, src_path: str, dst_path: str = None) -> None:
        """Copy a file from src_path to dst_path in the staging file system"""

        return fs.copy.copy_file(
            self.src_fs, src_path, self.stg_fs, dst_path or src_path
        )

    def makedirs(self, dirname: str):
        return self.stg_fs.makedirs(dirname)

    def exists(self, name: str):
        return self.stg_fs.exists(name)

    def isdir(self, name: str):
        return self.stg_fs.isdir(name)

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
            and self.sch_fs.exists(path)
            and "r" in mode.lower()
        ):
            # Copy from the source fs
            self.copy_from_sch(path)
        return self.stg_fs.open(path, mode=mode)


def md5(fhandle_getter):
    import hashlib

    hash_md5 = hashlib.md5()
    with fhandle_getter() as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
