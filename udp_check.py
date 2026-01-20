"""
udp_check.py

Performs a best-effort UDP connectivity check.
UDP is connectionless, so lack of response does not necessarily indicate failure.
"""

import socket
import time
from typing import Callable, Optional, Tuple


def udp_check(
    host: str,
    port: int,
    timeout: float = 3.0,
    log: Optional[Callable[[str], None]] = None
) -> Tuple[bool, str]:
    """
    Send a UDP probe packet to a host and port and wait for a response.

    Args:
        host: Target hostname or IP
        port: Target UDP port
        timeout: Receive timeout in seconds

    Returns:
        (success, detail):
            success: True if probe was sent successfully (response is optional)
            detail:  observation message
    """

    def _log(msg: str) -> None:
        if log:
            log(msg)

    # Port validation (avoid crash / undefined behavior)
    if not isinstance(port, int):
        return False, "Port must be an integer"
    if port < 1 or port > 65535:
        return False, "Port must be between 1 and 65535"

    try:
        _log(f"[UDP] Sending UDP probe to {host}:{port} (timeout={timeout}s)")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)

        message = b"UDP_DIAGNOSTIC_PROBE"
        start = time.perf_counter()

        # Send UDP packet (no handshake)
        sock.sendto(message, (host, port))

        try:
            data, addr = sock.recvfrom(1024)
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            sock.close()

            _log(f"[UDP] Response received from {addr} ({latency_ms} ms)")
            return True, f"Response received in {latency_ms} ms"

        except socket.timeout:
            sock.close()
            # Best-effort: no response doesn't imply failure
            return True, "No response received (UDP is connectionless)"

    except socket.gaierror as e:
        return False, f"Address resolution error: {e}"

    except OSError as e:
        return False, f"OS error during UDP probe: {e}"

    except Exception as e:
        return False, f"Unexpected error: {e}"


# Test this module
if __name__ == "__main__":
    import sys

    def log(msg: str) -> None:
        print(msg, file=sys.stderr)

    tests = [
        ("8.8.8.8", 53),          # DNS (may respond or not depending on network)
        ("pool.ntp.org", 123),    # NTP 
        ("localhost", 9999),      # likely no service
        ("google.com", 99999),    # invalid port
    ]

    for host, port in tests:
        print("-" * 50)
        ok, detail = udp_check(host, port, timeout=3.0, log=log)
        print(f"Result: success={ok}, detail={detail}")


