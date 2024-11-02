import libvirt
import time
import xml.etree.ElementTree as ET

# Threshold CPU usage percentage for autoscaling
CPU_THRESHOLD = 80.0
# Time to wait before next check (in seconds)
CHECK_INTERVAL = 5

# Connection to the hypervisor
conn = libvirt.open("qemu:///system")

def get_cpu_usage(domain):
    """Calculate CPU usage percentage for a domain."""
    # Get CPU time initially
    prev_stats = domain.getCPUStats(True)[0]
    prev_total = prev_stats['cpu_time']

    time.sleep(1)  # Wait 1 second

    # Get CPU time again
    curr_stats = domain.getCPUStats(True)[0]
    curr_total = curr_stats['cpu_time']

    # Calculate CPU usage percentage
    cpu_usage = (curr_total - prev_total) / (1e9 * CHECK_INTERVAL) * 100  # Convert ns to %
    return cpu_usage

def create_new_server():
    """Clones an existing server XML to create a new server."""
    base_domain = conn.lookupByName("server1")
    xml_desc = base_domain.XMLDesc(0)
    new_xml = xml_desc.replace("<name>server1</name>", "<name>server3</name>")

    # Load and modify the XML if needed (e.g., IP address update)
    new_domain = conn.defineXML(new_xml)
    new_domain.create()
    print("[AUTOSCALER] New server created: server3")

def monitor_and_autoscale():
    """Monitors CPU usage and performs autoscaling if needed."""
    while True:
        high_usage = False
        for domain_name in ["server1", "server2"]:
            try:
                domain = conn.lookupByName(domain_name)
                cpu_usage = get_cpu_usage(domain)
                print(f"[MONITOR] {domain_name} CPU usage: {cpu_usage}%")

                if cpu_usage > CPU_THRESHOLD:
                    high_usage = True

            except libvirt.libvirtError:
                print(f"[MONITOR] Unable to access {domain_name}")

        # If high usage detected, scale up
        if high_usage:
            print("[AUTOSCALER] High CPU usage detected, creating a new server...")
            create_new_server()
            break  # Exit after scaling for this demonstration

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_and_autoscale()
