"""Helpers for running rsync transfers to and from COSMA hosts."""

import glob
import shlex
import subprocess


HOSTS = {
    "COSMA": "dc-amvr1@login.cosma.dur.ac.uk",
    "COSMA5": "dc-amvr1@login5.cosma.dur.ac.uk",
    "COSMA5a": "dc-amvr1@login5a.cosma.dur.ac.uk",
    "COSMA5b": "dc-amvr1@login5b.cosma.dur.ac.uk",
    "COSMA5c": "dc-amvr1@login5c.cosma.dur.ac.uk",
    "COSMA6": "dc-amvr1@login6.cosma.dur.ac.uk",
    "COSMA6a": "dc-amvr1@login6a.cosma.dur.ac.uk",
    "COSMA6b": "dc-amvr1@login6b.cosma.dur.ac.uk",
    "COSMA7": "dc-amvr1@login7.cosma.dur.ac.uk",
    "COSMA7a": "dc-amvr1@login7a.cosma.dur.ac.uk",
    "COSMA7b": "dc-amvr1@login7b.cosma.dur.ac.uk",
    "COSMA8": "dc-amvr1@login8.cosma.dur.ac.uk",
    "cam": "dc-amvr1@login-cpu.hpc.cam.ac.uk",
}

# Backwards-compatible alias used by existing callers.
hosts = HOSTS

DEFAULT_HOST_TO_LOCAL_EXCLUDES = [
    "result.pickle",
    "phase_single_dataset__version_0.45.0.zip",
    "phase_2_single_dataset__version_0.45.0.zip",
]


def _get_host_address(host):
    """Return the SSH address for a configured host label."""
    try:
        return HOSTS[host]
    except KeyError as error:
        valid_hosts = ", ".join(sorted(HOSTS))
        raise ValueError(f"Unknown host '{host}'. Valid hosts: {valid_hosts}") from error


def _normalize_patterns(patterns):
    """Return include/exclude patterns as a clean list."""
    if patterns is None:
        return []
    return [pattern for pattern in patterns if pattern]


def _expand_local_source(source):
    """Expand local glob patterns so subprocess-based rsync preserves old behavior."""
    if glob.has_magic(source):
        matches = glob.glob(source)
        if matches:
            return matches
    return [source]


def _build_rsync_command(
    source,
    destination,
    update=True,
    include_patterns=None,
    exclude_patterns=None,
    include_directories=False,
):
    """Build an rsync argv list for a single transfer."""
    command = ["rsync", "-v", "-r"]

    if update:
        command.append("--update")

    if include_directories:
        command.extend(["--include", "*/"])

    for pattern in _normalize_patterns(include_patterns):
        command.extend(["--include", pattern])

    for pattern in _normalize_patterns(exclude_patterns):
        command.extend(["--exclude", pattern])

    command.extend([source, destination])
    return command


def _run_rsync(command):
    """Print and execute an rsync command."""
    print(shlex.join(command))
    return subprocess.run(command, check=True)


def rsync_local_to_host(
    path_to_file_local,
    path_to_file_host,
    host="COSMA7",
    update=True,
):
    """Rsync a local file or directory to a remote host path."""
    host_address = _get_host_address(host)
    destination = f"{host_address}:{path_to_file_host}"

    result = None
    for source in _expand_local_source(path_to_file_local):
        command = _build_rsync_command(
            source=source,
            destination=destination,
            update=update,
        )
        result = _run_rsync(command)
    return result


def rsync_host_to_local(
    path_to_file_host,
    path_to_file_local,
    host="COSMA7a",
    update=True,
):
    """Rsync a remote host path to a local file or directory."""
    source = f"{_get_host_address(host)}:{path_to_file_host}"
    command = _build_rsync_command(
        source=source,
        destination=path_to_file_local,
        update=update,
    )
    return _run_rsync(command)


def rsync_host_to_local_with_exclude(
    path_to_file_host,
    path_to_file_local,
    host="COSMA7a",
    update=True,
):
    """Rsync a remote path locally while excluding the default large result files."""
    source = f"{_get_host_address(host)}:{path_to_file_host}"
    command = _build_rsync_command(
        source=source,
        destination=path_to_file_local,
        update=update,
        exclude_patterns=DEFAULT_HOST_TO_LOCAL_EXCLUDES,
    )
    return _run_rsync(command)


def rsync_host_to_local_with_exclude_updated(
    path_to_file_host,
    path_to_file_local,
    host="COSMA7a",
    update=True,
    filenames=None,
):
    """Rsync a remote path locally while excluding custom filename patterns."""
    source = f"{_get_host_address(host)}:{path_to_file_host}"
    command = _build_rsync_command(
        source=source,
        destination=path_to_file_local,
        update=update,
        exclude_patterns=filenames,
    )
    return _run_rsync(command)


def rsync_host_to_local_with_include_updated(
    path_to_file_host,
    path_to_file_local,
    host="COSMA7a",
    update=True,
    filenames=None,
):
    """Rsync a remote path locally while including only selected filename patterns."""
    source = f"{_get_host_address(host)}:{path_to_file_host}"
    command = _build_rsync_command(
        source=source,
        destination=path_to_file_local,
        update=update,
        include_patterns=filenames,
        exclude_patterns=["*"],
        include_directories=True,
    )
    return _run_rsync(command)


def rsync_local_to_host_with_exclude_updated(
    path_to_file_local,
    path_to_file_host,
    host="COSMA7",
    update=True,
    filenames=None,
):
    """Rsync a local path to a host while excluding custom filename patterns."""
    host_address = _get_host_address(host)
    destination = f"{host_address}:{path_to_file_host}"

    result = None
    for source in _expand_local_source(path_to_file_local):
        command = _build_rsync_command(
            source=source,
            destination=destination,
            update=update,
            exclude_patterns=filenames,
        )
        result = _run_rsync(command)
    return result


def test__get_host_address():
    """Check that configured host lookup returns the expected address."""
    address = _get_host_address("COSMA7")
    if address != "dc-amvr1@login7.cosma.dur.ac.uk":
        raise ValueError("Unexpected host address for COSMA7")


def test__build_rsync_command_with_excludes():
    """Check that exclude patterns are inserted into the rsync argv list."""
    command = _build_rsync_command(
        source="source",
        destination="destination",
        update=True,
        exclude_patterns=["*.pickle", "*.zip"],
    )

    if "--update" not in command:
        raise ValueError("Expected --update in rsync command")
    if command.count("--exclude") != 2:
        raise ValueError("Expected two --exclude flags in rsync command")


def test__build_rsync_command_with_includes():
    """Check that include-only commands traverse directories and exclude everything else."""
    command = _build_rsync_command(
        source="source",
        destination="destination",
        update=False,
        include_patterns=["*.fits"],
        exclude_patterns=["*"],
        include_directories=True,
    )

    if command[:3] != ["rsync", "-v", "-r"]:
        raise ValueError("Unexpected base rsync command")
    if "--update" in command:
        raise ValueError("Did not expect --update in command")
    if command.count("--include") != 2:
        raise ValueError("Expected include flags for directories and patterns")


def test__expand_local_source():
    """Check that non-matching globs fall back to the original source string."""
    source = _expand_local_source("this_pattern_should_not_match_*.txt")
    if source != ["this_pattern_should_not_match_*.txt"]:
        raise ValueError("Expected unmatched glob pattern to be preserved")


def run_tests():
    """Run the module's internal non-network smoke tests."""
    test__get_host_address()
    test__build_rsync_command_with_excludes()
    test__build_rsync_command_with_includes()
    test__expand_local_source()


if __name__ == "__main__":
    run_tests()
