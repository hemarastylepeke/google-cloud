# GCP VM Deployment Script 🚀
This repository contains a Python script that automates the deployment of a Virtual Machine (VM) on Google Cloud Platform (GCP). The VM is configured with a static IP address, firewall rules for HTTP and SSH, and a simple "Hello World" webpage served using Nginx.
Features ✨

Automated VM Deployment: One-click deployment of a fully configured GCP VM
Static IP Configuration: Automatically creates or reuses a static IP address
Firewall Rules Setup: Creates firewall rules for HTTP (port 80) and SSH (port 22)
Web Server Installation: Installs and configures Nginx to serve a "Hello World" page
Error Handling: Comprehensive error handling and status reporting

## Prerequisites 📋
Before running the script, ensure you have:

Google Cloud SDK: Install and configure the Google Cloud SDK
Google Cloud Project: Create a project in Google Cloud and enable the Compute Engine API
IAM Permissions: Ensure your account has the following permissions:

compute.instances.create
compute.addresses.create
compute.firewalls.create


Python 3: Ensure Python 3 is installed on your system

## Installation & Usage 🔧
1. Clone the Repository
2. clone https://github.com/hemarastylepeke/google-cloud.git
cd google-cloud
3. Set Up Google Cloud SDK
Authenticate with your Google account
gcloud auth login

## Set your project
gcloud config set project YOUR_PROJECT_ID
3. Run the Deployment Script
Make the script executable
chmod +x deploy_vm.py

## Execute the script
./deploy_vm.py
4. Verify Deployment

Check the VM instance in the Google Cloud Console
Access the web server at http://<static-ip provided by the script>
SSH into the VM using the provided command

## How It Works 🔍
The script executes the following steps:

Retrieves Project ID from your gcloud configuration
Creates or Reuses a Static IP address named "web-server-static-ip"
Configures Firewall Rules to allow HTTP and SSH traffic
Deploys the VM Instance with the following configuration:

Machine type: e2-standard-2 (2 vCPUs, 8GB RAM)
Boot disk: 250GB, Ubuntu 20.04 LTS
Static IP address assigned
Nginx installation and configuration


## Outputs Deployment Details including VM name, IP, and access commands

Example Output 📝
CopyStarting deployment for project: cloud-vm-project-2025
Static IP address web-server-static-ip already exists. Reusing it.
Using static IP: 34.44.48.1
Firewall rule allow-http already exists. Skipping creation.
Firewall rule allow-ssh already exists. Skipping creation.
Creating VM instance...
Waiting for VM to initialize...
Deployment completed!
VM Name: web-server-vm
Static IP: 34.44.48.1
Access the web server at: http://34.44.48.1
SSH access: gcloud compute ssh web-server-vm --zone=us-central1-a
Troubleshooting 🔧
If you encounter issues, try these steps:
VM Not Running

Check VM status in the Google Cloud Console
Verify the Compute Engine API is enabled

Nginx Not Serving the Webpage
bashCopy# SSH into the VM
gcloud compute ssh web-server-vm --zone=us-central1-a

## Check Nginx status
sudo systemctl status nginx

## Verify the web page
curl http://localhost
Firewall Issues

Ensure firewall rules (allow-http and allow-ssh) exist
Verify the VM has the http-server tag

## Contributing 👥
Contributions are welcome! If you find any issues or have suggestions for improvement:

## License 📄
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments 🙏

Google Cloud Platform for providing the infrastructure
Nginx for the web server software
