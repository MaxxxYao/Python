"""
diagnostic_summary.py

Collects and summarizes diagnostic results from
DNS, TCP, UDP, and latency checks.
"""


def create_summary(hostname: str, ip: str):
    """
    Initialize a diagnostic summary structure.
    """
    return {
        "target": hostname,
        "ip_address": ip,
        "dns": None,
        "tcp": {},
        "udp": {},
        "latency": {},
        "overall_status": "UNKNOWN"
    }


def record_dns(summary: dict, success: bool, detail: str):
    summary["dns"] = {
        "success": success,
        "detail": detail
    }


def record_tcp(summary: dict, port: int, success: bool, detail: str):
    summary["tcp"][port] = {
        "success": success,
        "detail": detail
    }


def record_udp(summary: dict, port: int, success: bool, detail: str):
    summary["udp"][port] = {
        "success": success,
        "detail": detail
    }


def record_latency(summary: dict, port: int, success: bool, latency_ms):
    summary["latency"][port] = {
        "success": success,
        "latency_ms": latency_ms
    }


def evaluate_overall_status(summary: dict):
    """
    Decide overall reachability based on results.
    """
    if not summary["dns"]["success"]:
        summary["overall_status"] = "UNREACHABLE"
        return

    if any(not result["success"] for result in summary["tcp"].values()):
        summary["overall_status"] = "PARTIALLY REACHABLE"
        return

    summary["overall_status"] = "REACHABLE"


def print_summary(summary: dict, log=None):
    """
    Print a diagnostic summary.
    If log is provided, it will be used for output.
    Otherwise, print() is used.
    """
    log = log or print   

    log("\n" + "=" * 60)
    log("Diagnostic Summary")
    log("=" * 60)

    log(f"Target: {summary['target']}")
    log(f"IP Address: {summary['ip_address']}\n")

    dns = summary["dns"]
    dns_status = "PASS" if dns["success"] else "FAIL"
    log(f"DNS Resolution: {dns_status} ({dns['detail']})\n")

    log("TCP Connectivity:")
    for port, result in summary["tcp"].items():
        status = "PASS" if result["success"] else "FAIL"
        log(f"  - Port {port}: {status} ({result['detail']})")

    log("\nUDP Connectivity:")
    for port, result in summary["udp"].items():
        status = "PASS" if result["success"] else "WARN"
        log(f"  - Port {port}: {status} ({result['detail']})")

    log("\nLatency Measurements:")
    for port, result in summary["latency"].items():
        if result["success"]:
            log(f"  - Port {port}: {result['latency_ms']} ms")
        else:
            log(f"  - Port {port}: FAILED")

    log(f"\nOverall Status: {summary['overall_status']}")
    log("=" * 60)

