#!/usr/bin/env python3

import subprocess
import time
import sys

def run_command(command):
    """Run a shell command and return the output"""
    print(f"Executing: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error details: {e.stderr}")
        sys.exit(1)

def resource_exists(command):
    """Check if a resource exists by running a command that would fail if it doesn't"""
    try:
        subprocess.run(command, shell=True, check=True, text=True, 
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    # Variables - modify these as needed
    project_id = run_command("gcloud config get-value project").strip()
    vm_name = "web-server-vm"
    machine_type = "e2-standard-2"  # 2 vCPUs, 8GB RAM
    zone = "us-central1-a"
    region = "us-central1"
    boot_disk_size = "250GB"
    image_family = "ubuntu-2004-lts"
    image_project = "ubuntu-os-cloud"
    network_tag = "http-server"
    static_ip_name = "web-server-static-ip"
    
    print(f"Starting deployment for project: {project_id}")
    
    # Create a static IP address if it doesn't exist
    if not resource_exists(f"gcloud compute addresses describe {static_ip_name} --project={project_id} --region={region}"):
        print("Creating static IP address...")
        run_command(f"gcloud compute addresses create {static_ip_name} "
                   f"--project={project_id} "
                   f"--region={region}")
    else:
        print(f"Static IP address {static_ip_name} already exists. Reusing it.")
    
    # Get the static IP address
    static_ip = run_command(f"gcloud compute addresses describe {static_ip_name} "
                           f"--project={project_id} "
                           f"--region={region} "
                           f'--format="value(address)"').strip()
    
    print(f"Using static IP: {static_ip}")
    
    # Create firewall rule for HTTP if it doesn't exist
    if not resource_exists(f"gcloud compute firewall-rules describe allow-http --project={project_id}"):
        print("Creating firewall rule for HTTP...")
        run_command(f"gcloud compute firewall-rules create allow-http "
                   f"--project={project_id} "
                   f"--direction=INGRESS "
                   f"--priority=1000 "
                   f"--network=default "
                   f"--action=ALLOW "
                   f"--rules=tcp:80 "
                   f"--source-ranges=0.0.0.0/0 "
                   f"--target-tags={network_tag}")
    else:
        print("Firewall rule allow-http already exists. Skipping creation.")
    
    # Create firewall rule for SSH if it doesn't exist
    if not resource_exists(f"gcloud compute firewall-rules describe allow-ssh --project={project_id}"):
        print("Creating firewall rule for SSH...")
        run_command(f"gcloud compute firewall-rules create allow-ssh "
                   f"--project={project_id} "
                   f"--direction=INGRESS "
                   f"--priority=1000 "
                   f"--network=default "
                   f"--action=ALLOW "
                   f"--rules=tcp:22 "
                   f"--source-ranges=0.0.0.0/0 "
                   f"--target-tags={network_tag}")
    else:
        print("Firewall rule allow-ssh already exists. Skipping creation.")
    
    # Check if VM instance exists
    vm_exists = resource_exists(f"gcloud compute instances describe {vm_name} --project={project_id} --zone={zone}")
    
    if not vm_exists:
        # Create VM instance
        print("Creating VM instance...")
        startup_script = (
            '#!/bin/bash\n'
            'apt-get update\n'
            'apt-get install -y nginx\n'
            'echo "<html><body><h1>Hello World from $(hostname)</h1></body></html>" > /var/www/html/index.html'
        )
        
        run_command(f"gcloud compute instances create {vm_name} "
                   f"--project={project_id} "
                   f"--zone={zone} "
                   f"--machine-type={machine_type} "
                   f"--subnet=default "
                   f"--address={static_ip} "
                   f"--network-tier=PREMIUM "
                   f"--maintenance-policy=MIGRATE "
                   f"--tags={network_tag} "
                   f"--image-family={image_family} "
                   f"--image-project={image_project} "
                   f"--boot-disk-size={boot_disk_size} "
                   f"--boot-disk-type=pd-balanced "
                   f"--boot-disk-device-name={vm_name} "
                   f"--metadata=startup-script='{startup_script}'")
        
        # Wait a moment for the VM to start
        print("Waiting for VM to initialize...")
        time.sleep(30)
    else:
        print(f"VM instance {vm_name} already exists. Skipping creation.")
    
    print("Deployment completed!")
    print(f"VM Name: {vm_name}")
    print(f"Static IP: {static_ip}")
    print(f"Access the web server at: http://{static_ip}")
    print(f"SSH access: gcloud compute ssh {vm_name} --zone={zone}")

if __name__ == "__main__":
    main()
