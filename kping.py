import sys
import argparse
import socket
import time
from datetime import datetime
import logging
from typing import List

try:
    import requests
    requests_available = True
except ImportError:
    requests_available = False

VERSION = "0.1.0"
GREEN = '\033[92m'
RESET = '\033[0m'

def print_help():
    help_message = f"""
    --------------------------------------------------------------
    kping by Keane Audric
    Version: {VERSION}
    GitHub: https://github.com/KeaneAudric01
    --------------------------------------------------------------

    Usage: kping [-flags] server-address [server-port]

    Usage (full): kping [-t] [-n times] [-H host] [-p port] [-i interval] [-d] [-s] [-f] [-v timeout] [-q]

     -t     : ping continuously until stopped via control-c
     -n 5   : for instance, send 5 pings
     -H     : specify the host to ping
     -p     : specify the port to ping
     -i 1   : set the interval between pings (in seconds)
     -d     : include date and time on each line
     -s     : automatically exit on a successful ping
     -f     : verbose mode
     -v 1   : set custom timeout (in seconds)
     -q     : ping flood (send pings as fast as possible)
    """
    print(help_message)

def get_ip_organization(ip: str) -> str:
    if not requests_available:
        return "Unable to locate requests module"
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/org")
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Unknown"
    except requests.RequestException:
        return "Unknown"

def tcp_ping(host: str, port: int, count: int, continuous: bool, interval: int, include_datetime: bool, stop_on_success: bool, verbose: bool, timeout: int, ping_flood: bool):
    organization = get_ip_organization(host)
    attempt = 1
    success_count = 0
    fail_count = 0
    trip_times: List[float] = []

    try:
        while continuous or attempt <= count:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                start_time = time.time()
                try:
                    s.connect((host, port))
                    elapsed = (time.time() - start_time) * 1000
                    trip_times.append(elapsed)
                    success_count += 1
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if include_datetime else ""
                    print(f"{timestamp} Connected to {GREEN}{host} ({organization}){RESET}: icmp_seq={GREEN}{attempt}{RESET} time={GREEN}{elapsed:.2f}ms{RESET} protocol={GREEN}TCP{RESET} port={GREEN}{port}{RESET}")
                    if stop_on_success:
                        break
                except socket.error as e:
                    fail_count += 1
                    print(f"Unable to connect to {host}:{port} - {e}")
            attempt += 1
            if not ping_flood:
                time.sleep(interval)
    except KeyboardInterrupt:
        print("\nPing interrupted by user.")
    finally:
        print_statistics(success_count, fail_count, trip_times)

def print_statistics(success_count: int, fail_count: int, trip_times: List[float]):
    total_pings = success_count + fail_count
    fail_percentage = (fail_count / total_pings) * 100 if total_pings > 0 else 0
    min_time = min(trip_times) if trip_times else 0
    max_time = max(trip_times) if trip_times else 0
    avg_time = sum(trip_times) / len(trip_times) if trip_times else 0

    print("\nPing statistics:")
    print(f"    Packets: Sent = {total_pings}, Received = {success_count}, Lost = {fail_count} ({fail_percentage:.2f}% loss)")
    print(f"Approximate round trip times in milli-seconds:")
    print(f"    Minimum = {min_time:.2f}ms, Maximum = {max_time:.2f}ms, Average = {avg_time:.2f}ms")

def main():
    parser = argparse.ArgumentParser(description="A simple TCP ping tool.", add_help=False)
    parser.add_argument("--help", action="store_true", help="Show this help message and exit")
    parser.add_argument("-H", "--host", required=False, help="Target host to ping")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target port to ping (default: 80)")
    parser.add_argument("-n", "--count", type=int, default=5, help="Number of ping attempts (default: 5)")
    parser.add_argument("-t", "--continuous", action="store_true", help="Ping continuously until stopped")
    parser.add_argument("-i", "--interval", type=int, default=1, help="Interval between pings (in seconds)")
    parser.add_argument("-d", "--datetime", action="store_true", help="Include date and time on each line")
    parser.add_argument("-s", "--stop-on-success", action="store_true", help="Automatically exit on a successful ping")
    parser.add_argument("-f", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-v", "--timeout", type=int, default=1, help="Custom timeout (in seconds)")
    parser.add_argument("-q", "--ping-flood", action="store_true", help="Ping flood (send pings as fast as possible)")

    args = parser.parse_args()

    if args.help or not args.host:
        print_help()
        sys.exit(1)

    if args.continuous:
        print(f"Pinging {args.host} on port {args.port} continuously, press Ctrl+C to stop")
    else:
        print(f"Pinging {args.host} on port {args.port} with {args.count} requests")

    tcp_ping(args.host, args.port, args.count, args.continuous, args.interval, args.datetime, args.stop_on_success, args.verbose, args.timeout, args.ping_flood)

if __name__ == "__main__":
    main()
