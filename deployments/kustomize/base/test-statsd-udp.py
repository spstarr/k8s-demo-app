import socket

# Configuration for the statsd server
STATSD_HOST = 'otel-collector-opentelemetry-collector.opentelemetry.svc.cluster.local'
# NOTE: The standard StatsD UDP port is 8125.
# Ensure your OpenTelemetry Collector StatsD receiver configuration uses this port (or the one you specify).
STATSD_PORT = 8125 

# The statsd metric string
# Format: <name>:<value>|<type>
METRIC = 'helloworld.ok:200|g'

def send_statsd_metric_udp(host, port, metric):
    """Sends a single statsd metric string via UDP."""
    # 1. Unlike TCP, UDP StatsD metrics do NOT typically require a trailing newline character
    # However, some collectors might tolerate it, but it's cleaner to omit it for standard UDP StatsD.
    metric_bytes = metric.encode('utf-8')

    try:
        # 2. Create a UDP socket (AF_INET for IPv4, SOCK_DGRAM for UDP)
        # Note the change from SOCK_STREAM (TCP) to SOCK_DGRAM (UDP).
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 3. UDP is a connectionless protocol, so there is NO 'sock.connect()' call.

        # 4. Send the message. We use sendto(), which specifies the destination (host, port).
        # We don't use sendall() for UDP.
        print(f"Sending metric to {host}:{port} via UDP...")
        sock.sendto(metric_bytes, (host, port))

        print(f"Successfully sent metric: '{metric}' via UDP to {host}:{port}")

    except socket.error as e:
        # Note: UDP errors are often different from TCP (e.g., no 'Connection refused').
        # Errors here usually indicate problems with the local machine/network setup.
        print(f"Error sending metric via UDP: {e}")
        print("Please ensure your OpenTelemetry Collector's StatsD receiver is configured for UDP and running on the correct port (default 8125).")
    finally:
        # 5. Close the socket
        if 'sock' in locals():
            sock.close()

if __name__ == "__main__":
    send_statsd_metric_udp(STATSD_HOST, STATSD_PORT, METRIC)
