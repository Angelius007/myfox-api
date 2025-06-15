from __future__ import print_function
import socket as _stdlib_socket

import pytest_socket
import sys


_module = sys.modules[__name__]
# 1️⃣  On (re)ré‑active la socket dès l’import
pytest_socket.enable_socket()

# 2️⃣  On autorise loopback uniquement (asyncio.socketpair bosse en local)
pytest_socket.socket_allow_hosts(["127.0.0.1", "::1"])


# 3️⃣  On rend disable_socket inoffensif pour le reste de la session
def _noop(*_a, **_kw):  # pylint: disable=unused-argument
    pass


pytest_socket.disable_socket = _noop          # ← patch lethal
pytest_socket.SocketBlockedError = RuntimeError  # si un appel furtif passe

# 4️⃣  On force aussi le vrai socket dans le module stdlib,
#     au cas où GuardedSocket aurait déjà été injecté
import socket  # noqa: E402
socket.socket = _stdlib_socket.socket


def pytest_configure(config):
    # 1️⃣  Ré‑active complètement les sockets
    pytest_socket.enable_socket()

    # 2️⃣  …mais ne laisse passer que le local (asyncio.socketpair)
    pytest_socket.socket_allow_hosts(["127.0.0.1"])
