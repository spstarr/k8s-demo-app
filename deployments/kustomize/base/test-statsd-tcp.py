import socket

# Configuration for the statsd server
STATSD_HOST = 'otel-collector-opentelemetry-collector.opentelemetry.svc.cluster.local'
# NOTE: The standard StatsD TCP port is often 8126 (while UDP is 8125).
# Check your OpenTelemetry Collector StatsD receiver configuration for the exact port.
STATSD_PORT = 8125

# The statsd metric string
# Format: <name>:<value>|<type>
METRIC = 'helloworld.ok:200|g'

def send_statsd_metric_tcp(host, port, metric):
    """Sends a single statsd metric string via TCP."""
    # 1. Append a newline character, which is required for TCP StatsD
    metric_with_newline = metric + '\n'

    try:
        # 2. Create a TCP socket (AF_INET for IPv4, SOCK_STREAM for TCP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 3. Connect to the statsd server
        print(f"Connecting to {host}:{port}...")
        sock.connect((host, port))

        # 4. Encode the metric string to bytes
        message = metric_with_newline.encode('utf-8')

        # 5. Send the entire message
        sock.sendall(message)
        # We use sendall() for TCP to ensure the entire message is sent, even
        # if the buffer isn't large enough for a single send() call.

        print(f"Successfully sent metric: '{metric}' via TCP to {host}:{port}")

    except socket.error as e:
        print(f"Error sending metric via TCP: {e}")
        print("Please ensure your OpenTelemetry Collector's StatsD receiver is configured for TCP and running on the correct port (default 8126).")
    finally:
        # 6. Close the socket
        if 'sock' in locals() or 'sock' in globals():
            sock.close()

if __name__ == "__main__":
    send_statsd_metric_tcp(STATSD_HOST, STATSD_PORT, METRIC)
