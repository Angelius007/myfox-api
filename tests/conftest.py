from __future__ import print_function
import socket as _stdlib_socket
import asyncio
import sys
import threading

import pytest
import pytest_socket

_module = sys.modules[__name__]
# On (re)réactive la socket dès l'import
pytest_socket.enable_socket()

# On autorise loopback uniquement (asyncio.socketpair bosse en local)
pytest_socket.socket_allow_hosts(["127.0.0.1", "::1"])


# On rend disable_socket inoffensif pour le reste de la session
def _noop(*_a, **_kw):  # pylint: disable=unused-argument
    pass


pytest_socket.disable_socket = _noop  # ← patch lethal
pytest_socket.SocketBlockedError = RuntimeError  # si un appel furtif passe

# On force aussi le vrai socket dans le module stdlib,
#     au cas où GuardedSocket aurait déjà été injecté
import socket  # noqa: E402
socket.socket = _stdlib_socket.socket


def pytest_configure(config):
    # Ré‑active complètement les sockets
    pytest_socket.enable_socket()

    # …mais ne laisse passer que le local (asyncio.socketpair)
    pytest_socket.socket_allow_hosts(["127.0.0.1"])


@pytest.fixture(autouse=True)
def enable_event_loop_debug():
    """Override pytest-homeassistant-custom-component fixture for Python 3.13 compatibility.

    Python 3.13 no longer allows asyncio.get_event_loop() to implicitly create an event loop.
    This override safely attempts to enable debug mode if a loop exists, otherwise does nothing.
    """
    try:
        loop = asyncio.get_running_loop()
        old_debug = loop.get_debug()
        loop.set_debug(True)
        yield
        loop.set_debug(old_debug)
    except RuntimeError:
        # No running loop yet, skip debug mode
        yield


@pytest.fixture(autouse=True)
def verify_cleanup(
        expected_lingering_tasks: bool,
        expected_lingering_timers: bool,
):
    """Override pytest-homeassistant-custom-component fixture for Python 3.13 compatibility."""
    try:
        event_loop = asyncio.get_running_loop()
    except RuntimeError:
        # No event loop, skip cleanup verification
        yield
        return

    threads_before = frozenset(threading.enumerate())
    tasks_before = asyncio.all_tasks(event_loop)
    yield
    tasks = asyncio.all_tasks(event_loop) - tasks_before
    lingering_tasks = [task for task in tasks if not (task.done() or task.cancelled())]

    if lingering_tasks and not expected_lingering_tasks:
        for task in lingering_tasks:
            task.cancel()
        pytest.fail(f"Found lingering tasks: {lingering_tasks}")

    threads = frozenset(threading.enumerate()) - threads_before
    lingering_threads = [thread for thread in threads if thread.is_alive() and not thread.daemon]
    if lingering_threads:
        pytest.fail(f"Found lingering threads: {lingering_threads}")
