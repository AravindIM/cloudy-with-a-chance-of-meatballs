#!/usr/bin/env python3

"""Run the autoscaler to monitor and scale."""


import libvirt
import sys
import time
import socket


MAIN_SERVER = "server"
AUX_SERVER = "server-clone"
CPU_THRESHOLD = 95
POOL_TIME = 2
SCALE = 10**9
CLIENT_IP = "127.0.0.1"
CLIENT_PORT = 6009
BUFFER_SIZE = 2048
AUX_IP = "192.168.122.3"
AUX_PORT = 8008


class Autoscaler:
    """Scale the vms according to the threshold."""

    def __init__(self):
        """Initialize the autoscaler object."""
        try:
            self.connection = libvirt.open("qemu:///system")
            for domain in self.connection.listAllDomains():
                if domain.name() == MAIN_SERVER:
                    continue
                if domain.isActive():
                    domain.shutdown()
                    while domain.isActive():
                        time.sleep(0.5)
                else:
                    continue
            print("Starting Autoscaler... [OK]")
        except libvirt.libvirtError:
            print("ERROR: Connection to Hypervisor failed")
            sys.exit(1)

    def cpu_usage(self, name, pool_time=0.5, scale=10**9):
        """Monitor the CPU usage."""
        scale_factor = pool_time * scale
        try:
            domain = self.connection.lookupByName(name)
        except libvirt.libvirtError:
            print(f"ERROR: No domain found with the name {name}")
            sys.exit(1)
        prev_stats = domain.getCPUStats(True)[0]
        time.sleep(pool_time)
        curr_stats = domain.getCPUStats(True)[0]
        cpu_percent = 100 * (curr_stats['cpu_time']
                             - prev_stats['cpu_time']) / scale_factor
        if cpu_percent > 100:
            cpu_percent = 100

        return cpu_percent

    def scale(self, name):
        """Scales the vm."""
        aux_domain = self.connection.lookupByName(AUX_SERVER)
        print("Starting VM Monitor... [OK]")
        while True:
            cpu_usage = self.cpu_usage(name, POOL_TIME, SCALE)
            print(f"CPU usage of {name}: {cpu_usage}")
            if cpu_usage > CPU_THRESHOLD and not aux_domain.isActive():
                try:
                    aux_domain.create()
                    print("Booting up aux server...")
                    while not aux_domain.isActive() or not self.check_port_open():
                        time.sleep(1)
                    self.notify_client()
                    print(f"Aux server - {AUX_SERVER} [{AUX_IP}] is now up and running... [OK]")
                except Exception as e:
                    print(f"ERROR: Failed launching aux server. {e}")

    def check_port_open(self):
        """Check if aux port open."""
        try:
            aux_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            aux_sock.connect((AUX_IP, AUX_PORT))
            return True
        except Exception:
            return False

    def notify_client(self):
        """Notify client that the new aux server is up."""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((CLIENT_IP, CLIENT_PORT))
        client.send(AUX_IP.encode())


def main():
    """Run the autoscaler."""
    autoscaler = Autoscaler()
    autoscaler.scale(MAIN_SERVER)


if __name__ == "__main__":
    main()
