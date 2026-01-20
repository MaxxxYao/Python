import socket
import time
from typing import Callable, Tuple, Optional


def tcp_check(
    host: str,
    port: int,
    timeout: float = 3.0,
    log: Optional[Callable[[str], None]] = None
) -> Tuple[bool, str, Optional[float]]:
    """
    Attempt a TCP connection and measure connect latency.

    Args:
        host: target IP address
        port: TCP port to test
        timeout: socket timeout in seconds
        log: optional logging function (e.g. stderr logger)

    Returns:
        success (bool)
        detail (str)
        latency_ms (float | None)
    """

    def _log(msg: str):
        if log:
            log(msg)

    # Port validation
    if not isinstance(port, int):
        return False, "Port must be an integer", None
    if port < 1 or port > 65535:
        return False, "Port must be between 1 and 65535", None

    try:
        _log(f"[TCP] Testing TCP connectivity to {host}:{port} (timeout={timeout}s)")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        start = time.perf_counter()
        sock.connect((host, port))
        end = time.perf_counter()

        latency_ms = round((end - start) * 1000, 2)
        sock.close()

        return True, f"Connection successful ({latency_ms} ms)", latency_ms

    except socket.timeout:
        return False, "TCP connection timed out", None

    except ConnectionRefusedError:
        return False, "Connection refused (RST)", None

    except OSError as e:
        return False, f"OS error: {e}", None

    except Exception as e:
        return False, f"Unexpected error: {e}", None
