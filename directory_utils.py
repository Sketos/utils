"""Utilities for creating, updating, and moving directories."""

import os
from pathlib import Path
import shutil
import tempfile


def _to_path(directory):
    """Convert a directory-like input into a `Path` object."""
    return Path(directory).expanduser()


def get_list_of_directory_trees_in_directory(directory):
    """Return every directory discovered by recursively walking `directory`."""
    directory_path = _to_path(directory)
    return [root for root, _, _ in os.walk(directory_path)]


def create_directory(directory):
    """Create a directory and any missing parents, then return its path."""
    directory_path = _to_path(directory)
    directory_path.mkdir(parents=True, exist_ok=True)
    return str(directory_path)


def create_nested_directory(directory):
    """Compatibility wrapper around `create_directory`."""
    return create_directory(directory=directory)


def create_directory_tree_from_list_of_strings(
    list_of_strings,
    base_directory_of_directory_tree="",
):
    """Create nested directories from a sequence of folder names."""
    directory_tree = _to_path(base_directory_of_directory_tree or ".")

    for name in list_of_strings:
        if name:
            directory_tree = directory_tree / name
            directory_tree.mkdir(parents=True, exist_ok=True)

    return str(directory_tree)


def update_directory_with_folder_names(
    directory,
    folder_names,
    make=False,
    raise_error=True,
):
    """Append folder names to a base directory, optionally creating them."""
    directory_updated = _to_path(sanitize_directory(directory=directory))

    if not directory_updated.is_dir():
        raise IOError(f"The directory {directory} does not exist")

    for name in folder_names:
        directory_updated = directory_updated / name

        if make:
            directory_updated.mkdir(parents=True, exist_ok=True)
            continue

        if not directory_updated.is_dir():
            if raise_error:
                raise IOError(f"The directory {directory_updated} does not exist")
            return str(directory_updated)

    return str(directory_updated)


def sanitize_directory(directory):
    """Remove a trailing directory separator while preserving root directories."""
    directory_str = str(directory)

    if directory_str in {"/", "."}:
        return directory_str

    return directory_str.rstrip("/\\")


def move_directory_to_path(directory, path):
    """Move a directory into another existing directory and return the new path."""
    directory_path = _to_path(directory)
    path_to_move_into = _to_path(path)

    if not directory_path.is_dir():
        raise IOError(f"The directory {directory} does not exist")
    if not path_to_move_into.is_dir():
        raise IOError(f"The directory {path} does not exist")

    destination = path_to_move_into / directory_path.name
    shutil.move(str(directory_path), str(path_to_move_into))
    return str(destination)


def test__sanitize_directory():
    """Check that a trailing slash is removed from a normal directory path."""
    directory_i = "./folder1/folder2/"
    directory_o = "./folder1/folder2"

    directory_i = sanitize_directory(directory=directory_i)

    if directory_i != directory_o:
        raise ValueError("sanitize_directory did not remove the trailing slash")


def test__create_directory():
    """Check that nested directories are created successfully."""
    with tempfile.TemporaryDirectory() as temp_dir:
        target = Path(temp_dir) / "level_1" / "level_2"
        created = create_directory(str(target))
        if not Path(created).is_dir():
            raise ValueError("create_directory did not create the target path")


def test__create_directory_tree_from_list_of_strings():
    """Check that a folder-name list is converted into nested directories."""
    with tempfile.TemporaryDirectory() as temp_dir:
        created = create_directory_tree_from_list_of_strings(
            list_of_strings=["a", "b", "c"],
            base_directory_of_directory_tree=temp_dir,
        )
        if not Path(created).is_dir():
            raise ValueError("create_directory_tree_from_list_of_strings failed")
        if Path(created).name != "c":
            raise ValueError("Unexpected final directory name")


def test__update_directory_with_folder_names():
    """Check that directory updates work both with and without creation."""
    with tempfile.TemporaryDirectory() as temp_dir:
        base = Path(temp_dir)
        create_directory(base / "existing")

        updated = update_directory_with_folder_names(
            directory=str(base),
            folder_names=["existing"],
            make=False,
        )
        if not Path(updated).is_dir():
            raise ValueError("update_directory_with_folder_names should find existing paths")

        created = update_directory_with_folder_names(
            directory=str(base),
            folder_names=["new_1", "new_2"],
            make=True,
        )
        if not Path(created).is_dir():
            raise ValueError("update_directory_with_folder_names should create missing paths")


def test__move_directory_to_path():
    """Check that a directory is moved into the requested destination directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        source_parent = temp_path / "source_parent"
        destination_parent = temp_path / "destination_parent"
        source = source_parent / "folder_to_move"

        create_directory(source)
        create_directory(destination_parent)

        moved = move_directory_to_path(str(source), str(destination_parent))

        if Path(source).exists():
            raise ValueError("Source directory should no longer exist after move")
        if not Path(moved).is_dir():
            raise ValueError("Moved directory was not found in the destination path")


def run_tests():
    """Run the module's self-contained smoke tests."""
    test__sanitize_directory()
    test__create_directory()
    test__create_directory_tree_from_list_of_strings()
    test__update_directory_with_folder_names()
    test__move_directory_to_path()


if __name__ == "__main__":
    run_tests()
