"""
main.py

Mini Network Diagnostic Tool (argparse version)
Usage examples:
  python main.py google.com
  python main.py google.com --tcp 80 443 --udp 53 --timeout 3
"""

import argparse
import json
import sys

from diagnostic_summary import (
    create_summary,
    evaluate_overall_status,
    print_summary,
    record_dns,
    record_latency,
    record_tcp,
    record_udp,
)
from dns_check import dns_check
from tcp_check import tcp_check
from udp_check import udp_check


DEFAULT_TCP_PORTS = [80, 443]
DEFAULT_UDP_PORTS = [53]


def log(message: str) -> None:
    """Print logs to stderr so stdout can be reserved for JSON output."""
    print(message, file=sys.stderr)


def valid_port(p: str) -> int:
    """argparse type validator for port numbers."""
    port = int(p)
    if port < 1 or port > 65535:
        raise argparse.ArgumentTypeError("Port must be 1-65535")
    return port


def parse_args():
    parser = argparse.ArgumentParser(
        description="Mini Network Diagnostic Tool: DNS + TCP/UDP + Latency + Summary"
    )

    parser.add_argument(
        "target",
        help="Target hostname or IP address (e.g., google.com or 8.8.8.8)",
    )

    parser.add_argument(
        "--tcp",
        nargs="+",
        type=valid_port,
        default=DEFAULT_TCP_PORTS,
        help="TCP ports to test (default: 80 443)",
    )

    parser.add_argument(
        "--udp",
        nargs="+",
        type=valid_port,  # keep consistent validation
        default=DEFAULT_UDP_PORTS,
        help="UDP ports to test (default: 53, best-effort)",
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=3.0,
        help="Socket timeout in seconds (default: 3.0)",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output the diagnostic summary as JSON (machine-readable)",
    )

    parser.add_argument(
        "--json-out",
        type=str,
        default=None,
        help="Write JSON output to a file (e.g., result.json)",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    hostname = args.target.strip()
    tcp_ports = args.tcp
    udp_ports = args.udp
    timeout = args.timeout

    if not hostname:
        log("Error: target cannot be empty.")
        return

    # Header / run config logs (stderr)
    log("=" * 60)
    log(" Mini Network Diagnostic Tool ")
    log("=" * 60)
    log(f"Target: {hostname}")
    log(f"TCP ports: {tcp_ports}")
    log(f"UDP ports: {udp_ports} (best-effort)")
    log(f"Timeout: {timeout}s")
    log("=" * 60)

    # DNS Resolution
    dns_ok, dns_result = dns_check(hostname, log=log)
    if not dns_ok:
        summary = create_summary(hostname, None)
        record_dns(summary, False, dns_result)
        evaluate_overall_status(summary)

        if args.json:
            json_text = json.dumps(summary, indent=2)
            print(json_text)
            if args.json_out:
                with open(args.json_out, "w", encoding="utf-8") as f:
                    f.write(json_text)
            return

        print_summary(summary, log=log)
        

    ip_address = dns_result
    summary = create_summary(hostname, ip_address)
    record_dns(summary, True, f"Resolved to {ip_address}")

    # TCP Connectivity Check (also captures latency)
    for port in tcp_ports:
        ok, detail, latency_ms = tcp_check(ip_address, port, timeout=timeout, log=log)
        record_tcp(summary, port, ok, detail)

        if ok and latency_ms is not None:
            record_latency(summary, port, True, latency_ms)
        else:
            record_latency(summary, port, False, None)

    # UDP Connectivity Check 
    for port in udp_ports:
        ok, detail = udp_check(ip_address, port, timeout=timeout, log=log)
        record_udp(summary, port, ok, detail)

    # Final Evaluation & Output
    evaluate_overall_status(summary)
    print_summary(summary, log=log)

    if args.json:
        json_text = json.dumps(summary, indent=2)
        print(json_text)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            f.write(json_text)
    






if __name__ == "__main__":
    main()
