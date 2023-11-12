import subprocess
import platform
import time
import notify2

def send_notification(message):
    notify2.init("Connection status")
    n = notify2.Notification("Port Status Update", message)
    n.show()

def block_all_connections():
    system = platform.system()
    if system == 'Linux':
        try:
            # Flush existing rules
            subprocess.run(['sudo', 'iptables', '-F'])
            
            # Block all incoming and outgoing connections
            subprocess.run(['sudo', 'iptables', '-P', 'INPUT', 'DROP'])
            subprocess.run(['sudo', 'iptables', '-P', 'OUTPUT', 'DROP'])
            
            send_notification("All connections blocked on Linux.")
        except Exception as e:
            send_notification(f"Error blocking connections on Linux: {e}")
    elif system == 'Windows':
        try:
            # Block all incoming and outgoing connections on Windows
            subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'firewallpolicy', 'blockinbound,blockoutbound'])
            
            send_notification("All connections blocked on Windows.")
        except Exception as e:
            send_notification(f"Error blocking connections on Windows: {e}")
    else:
        send_notification("Unsupported operating system.")

def enable_all_connections():
    system = platform.system()
    if system == 'Linux':
        try:
            # Reset iptables rules to default (allow all)
            subprocess.run(['sudo', 'iptables', '-F'])
            subprocess.run(['sudo', 'iptables', '-P', 'INPUT', 'ACCEPT'])
            subprocess.run(['sudo', 'iptables', '-P', 'OUTPUT', 'ACCEPT'])
            
            send_notification("Connections re-enabled on Linux.")
        except Exception as e:
            send_notification(f"Error enabling connections on Linux: {e}")
    elif system == 'Windows':
        try:
            # Reset firewall rules to default (allow all)
            subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'firewallpolicy', 'allowinbound,allowoutbound'])
            
            send_notification("Connections re-enabled on Windows.")
        except Exception as e:
            send_notification(f"Error enabling connections on Windows: {e}")
    else:
        send_notification("Unsupported operating system.")

if __name__ == "__main__":
    # Block connections
    block_all_connections()

    # Wait for a few seconds (simulate some time passing)
    time.sleep(60)

    # Re-enable connections
    enable_all_connections()
