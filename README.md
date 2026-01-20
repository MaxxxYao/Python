Mini Network Diagnostic Tool 
================================================

Overview

This is a small  project in Python that demonstrates networking fundamentals by running basic diagnostics on a target hostname/IP:
DNS resolution, TCP connectivity, UDP best-effort probe, and TCP-based latency measurement. It outputs a structured summary and can also export JSON.

Features

- DNS Resolution: resolve hostname -> IPv4
- TCP Check: connect to specified ports + measure connect latency (ms)
- UDP Check (Best-effort): send a UDP probe; “no response” is normal for UDP
- Summary: aggregates results + overall status (REACHABLE / PARTIALLY REACHABLE / UNREACHABLE)
- JSON Output: JSON goes to stdout; logs/summary go to stderr (easy to redirect)

Requirements

- Python 3.x
- Standard library only 

Usage

Default ports: TCP 80 443, UDP 53, timeout 3.0s
Example:
  python main.py google.com

Custom ports / timeout:
Example:
  python main.py google.com --tcp 80 443 --udp 53 --timeout 2

JSON output (stdout):
Example:
  python main.py google.com --json
  python main.py google.com --json --json-out result.json

Split JSON + logs (Windows PowerShell):
Example:
  py main.py google.com --json 1> out.json 2> run.log

Project Files

- main.py: main countrol that uses all the modules to output summaries
- dns_check.py: DNS resolution
- tcp_check.py: TCP connectivity + latency
- udp_check.py: UDP probe 
- diagnostic_summary.py: collects results + prints summary

