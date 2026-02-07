# Cloudy with a Chance of Meatballs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

**An automated load balancer and autoscaling solution for managing distributed server workloads on virtualized infrastructure.**

## Overview

Cloudy with a Chance of Meatballs is an intelligent load balancing and autoscaling system designed to dynamically distribute client requests across multiple virtual machines based on real-time CPU utilization metrics. When system load exceeds configured thresholds, the autoscaler automatically provisions additional compute resources to maintain performance and reliability.

This project demonstrates practical concepts in distributed systems, resource management, and automated infrastructure scaling using libvirt-based virtual machine orchestration.

## Features

- **Intelligent Autoscaling**: Monitors CPU usage and automatically spawns additional VM instances when thresholds are exceeded
- **Load Balancing**: Distributes incoming client connections across multiple server instances
- **Real-time Monitoring**: Continuous CPU usage monitoring with configurable polling intervals
- **Automatic Resource Cleanup**: Gracefully shuts down auxiliary servers when no longer needed
- **Multi-threaded Architecture**: Handles concurrent client connections efficiently
- **Service Integration**: SystemD service file for seamless server deployment
- **Dynamic Server Discovery**: Clients automatically discover and connect to newly provisioned servers

## Tech Stack

- **Language**: Python 3.6+
- **Virtualization**: libvirt (KVM/QEMU)
- **Networking**: Python sockets (TCP/IP)
- **Concurrency**: Python threading
- **Service Management**: SystemD

## Architecture

The system consists of three main components:

1. **Server** (`myserver.py`): Accepts client connections, performs computational work (fibonacci calculations), and responds to requests
2. **Client** (`myclient.py`): Generates load by creating multiple concurrent connections to servers and sending workload requests
3. **Autoscaler** (`myautoscaler.py`): Monitors primary server CPU usage and manages auxiliary server lifecycle

### Data Flow

```
       CLIENT THREADS
    (Multiple concurrent
     connections)
            |
    ________|________
   |                 |
   v                 v
PRIMARY          AUXILIARY
SERVER (VM)      SERVER (VM)
192.168.122.2    192.168.122.3
   |                 |
   |_________________|
            |
            v
       AUTOSCALER
    (Monitors & Scales)
```

## Prerequisites

- **Python 3.6 or higher**
- **libvirt and KVM/QEMU**: For virtualization support
- **Two pre-configured virtual machines**:
  - Primary VM named `server` with IP `192.168.122.2`
  - Auxiliary VM named `server-clone` with IP `192.168.122.3`
- **Root/sudo access**: Required for libvirt operations and VM management
- **Linux-based OS**: Currently tested on Linux systems with libvirt support

### Installation & Setup

#### 1. Install Required Dependencies

```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip libvirt-dev libvirt0

# Fedora/RHEL
sudo dnf install python3 python3-devel libvirt-devel
```

#### 2. Install Python Dependencies

```bash
pip3 install libvirt-python
```

#### 3. Configure Virtual Machines

Create two VMs in libvirt with the following specifications:

```bash
# VM 1: Primary Server
Name: server
IP: 192.168.122.2
Port: 8008

# VM 2: Auxiliary Server (spawned by autoscaler)
Name: server-clone
IP: 192.168.122.3
Port: 8008
```

#### 4. Deploy Server Service

Copy the service file to your VM instances:

```bash
sudo cp myserver.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable myserver.service
```

Then start the service on both VMs:

```bash
sudo systemctl start myserver.service
sudo systemctl status myserver.service
```

## Usage

The system operates in a three-component workflow. Start each component in the order shown:

### Step 1: Start the Autoscaler

Run the autoscaler on your host machine to monitor the primary server and manage auxiliary server scaling:

```bash
python3 myautoscaler.py
```

**Output Example:**

```text
Starting Autoscaler... [OK]
Starting VM Monitor... [OK]
CPU usage of server: 5.2
CPU usage of server: 48.7
CPU usage of server: 98.3
Booting up aux server...
Aux server - server-clone [192.168.122.3] is now up and running... [OK]
```

### Step 2: Start the Client

Run the client with a specified number of worker threads and per-thread workload duration:

**Low Load Scenario** (1 thread, 1 second workload):

```bash
python3 myclient.py 1 1
```

**High Load Scenario** (10 threads, 5 second workload):

```bash
python3 myclient.py 10 5
```

**Output Example:**

```text
[Thread1]: Connecting to server 192.168.122.2 ... [OK]
[Thread1]: Sending message to server 192.168.122.2 ... [OK]
[Thread1]: Recieved response from server 192.168.122.2 ... [OK]
[Thread1]: Response from 192.168.122.2: DONE
```

### Step 3: Monitor Results

Observe the autoscaler console for CPU usage metrics and scaling events. The autoscaler will:

1. Continuously monitor primary server CPU usage
2. When CPU > 95% and auxiliary server is down, provision the auxiliary server
3. Notify the client of the new server IP
4. Client automatically begins balancing load across both servers

## Configuration

### Autoscaler Configuration

Edit `myautoscaler.py` to adjust these parameters:

```python
MAIN_SERVER = "server"          # Primary VM domain name
AUX_SERVER = "server-clone"     # Auxiliary VM domain name
CPU_THRESHOLD = 95              # CPU usage threshold (%) to trigger scaling
POOL_TIME = 2                   # Monitoring poll interval (seconds)
AUX_IP = "192.168.122.3"        # Auxiliary server IP address
AUX_PORT = 8008                 # Server listening port
CLIENT_IP = "127.0.0.1"         # Client notification port
CLIENT_PORT = 6009              # Client notification port
```

### Client Configuration

Edit `myclient.py` to adjust these parameters:

```python
SERVER_IP = "192.168.122.2"     # Primary server IP
SERVER_PORT = 8008              # Server listening port
BUFFER_SIZE = 2048              # Socket buffer size
```

### Server Configuration

Edit `myserver.py` to adjust these parameters:

```python
SOCKET_IP = "0.0.0.0"           # Bind to all interfaces
SOCKET_PORT = 8008              # Server listening port
BUFFER_SIZE = 2048              # Socket buffer size
MAX_CONNECTIONS = 10000         # Max concurrent connections
```

## Project Structure

```text
cloudy-with-a-chance-of-meatballs/
├── myserver.py              # Server component - handles client connections
├── myclient.py              # Client component - generates load
├── myautoscaler.py          # Autoscaler component - monitors and scales
├── myserver.service         # SystemD service file for server deployment
├── README.md                # This file
├── readme.txt               # Original project notes
├── LICENSE                  # MIT License
└── .gitignore               # (recommended) Git ignore file
```

### Component Details

- **myserver.py**: TCP server that listens for connections on port 8008. Accepts time intervals from clients, performs CPU-bound work (fibonacci calculations), and responds with completion status.

- **myclient.py**: Multi-threaded client that creates concurrent connections to servers, sends workload durations, and receives responses. Listens for autoscaler notifications about newly provisioned servers.

- **myautoscaler.py**: Libvirt-based orchestrator that monitors CPU usage of the primary server and manages auxiliary VM lifecycle based on configurable CPU thresholds.

## How It Works

1. **Initialization**: Autoscaler connects to libvirt, shuts down any running auxiliary servers, and begins monitoring CPU usage of the primary server at regular intervals.

2. **Normal Operation**: Client threads periodically send requests to the primary server. Server processes requests and responds.

3. **Scaling Trigger**: When CPU usage of the primary server exceeds 95%, the autoscaler boots the auxiliary server (`server-clone`).

4. **Server Notification**: Once the auxiliary server is online and responding, the autoscaler notifies the client of the new server IP.

5. **Load Balancing**: Client threads now randomly distribute requests between the primary and auxiliary servers, reducing load.

6. **Graceful Shutdown**: When load decreases, the autoscaler can shut down the auxiliary server (manual or automatic, depending on implementation).

## Troubleshooting

### "Connection to Hypervisor failed"

- Ensure libvirt is installed and running: `sudo systemctl status libvirtd`
- Check permissions: `sudo usermod -a -G libvirt $USER`
- Restart the user session or use `sudo` to run the autoscaler

### Client Cannot Connect to Server

- Verify server service is running on both VMs: `systemctl status myserver.service`
- Check network connectivity: `ping 192.168.122.2` and `ping 192.168.122.3`
- Verify firewall allows port 8008: `sudo firewall-cmd --add-port=8008/tcp --permanent`

### Auxiliary Server Not Spawning

- Verify the auxiliary VM exists in libvirt: `virsh list --all`
- Check CPU threshold setting in `myautoscaler.py` (default: 95%)
- Verify auxiliary VM can start manually: `virsh start server-clone`

## Roadmap & Future Improvements

- [ ] Configurable load balancing strategies (round-robin, least-connections, etc.)
- [ ] Graceful auxiliary server shutdown when load decreases
- [ ] Metrics and monitoring dashboard (Prometheus/Grafana integration)
- [ ] Multi-tier autoscaling with more than two server instances
- [ ] Containerized deployment support (Docker/Kubernetes)
- [ ] Enhanced logging and audit trails
- [ ] Unit and integration tests
- [ ] Performance benchmarking suite
- [ ] Configuration file support (YAML/JSON)

## Contributing

Contributions are welcome! To contribute to this project:

1. **Fork** the repository
2. **Create a feature branch** (`git checkout -b feature/your-feature`)
3. **Commit your changes** (`git commit -am 'Add new feature'`)
4. **Push to the branch** (`git push origin feature/your-feature`)
5. **Submit a Pull Request** with a clear description of changes

Please ensure:

- Code follows PEP 8 style guidelines
- Changes include appropriate documentation
- Commits have clear, descriptive messages

## Testing & Development

To extend or debug the system:

```bash
# Run autoscaler in debug mode with verbose output
python3 -u myautoscaler.py

# Test server independently
python3 myserver.py  # Runs on port 8008

# Test client connection (requires running server)
python3 myclient.py 1 2  # 1 thread, 2-second workload
```

## Deployment

### Local Development

Follow the Installation & Setup section above with local VMs.

### Production Deployment

For production use:

1. Use proper configuration management (e.g., environment variables or config files)
2. Implement proper logging and monitoring
3. Set up alerting for scaling events
4. Use load balancers with health checks
5. Consider using container orchestration (Kubernetes) for better scalability
6. Implement graceful shutdown mechanisms
7. Add persistent storage for metrics and logs

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright © 2023 Aravind I M**

## Authors & Maintainers

### Original Project Team (Group 5)

- Aravind I M - Primary Maintainer
- Faseem Shanavas
- Abhinav Ajithkumar
- Amal Firosh Thayyil

**Questions or Issues?** Feel free to open an issue on GitHub or contact the maintainers.

---

**Built with ❤️ for distributed systems enthusiasts**
