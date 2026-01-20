"""
dns_check.py

Performs DNS resolution for a given hostname.
This step verifies whether the hostname can be successfully
translated into an IP address before any TCP/UDP communication.
"""

import socket
from typing import Callable, Optional, Tuple


def dns_check(
    hostname: str,
    log: Optional[Callable[[str], None]] = None
) -> Tuple[bool, str]:
    """
    Resolve a hostname to an IPv4 address.

    Args:
        hostname: The domain name to resolve (e.g. "google.com")
        log: Optional logging function (e.g. stderr logger)

    Returns:
        (success, result):
            success: True if resolution succeeded
            result:  IPv4 address on success, error message on failure
    """

    def _log(msg: str) -> None:
        if log:
            log(msg)

    # Basic type check (defensive)
    if not isinstance(hostname, str):
        return False, "Hostname must be a string"

    try:
        _log(f"[DNS] Resolving hostname: {hostname}")

        ip_address = socket.gethostbyname(hostname)

        _log(f"[DNS] Resolution successful: {ip_address}")
        return True, ip_address

    except socket.gaierror as e:
        return False, f"DNS resolution failed: {e}"

    except UnicodeError:
        return False, "Invalid hostname encoding"

    except socket.timeout:
        return False, "DNS request timed out"

    except OSError as e:
        return False, f"Unexpected OS error: {e}"

    except Exception as e:
        return False, f"Unexpected error: {e}"



#Test in this module
if __name__ == "__main__":
    test_domains = [
        "google.com",          
        "nonexistent1234.com",  
        "",                    
        None,                  
        "谷歌.com"             
    ]

    for domain in test_domains:
        print("-" * 50)
        success, result = dns_check(domain)
        print(f"Result: success={success}, detail={result}")

