# -*- coding: utf-8 -*-

# Import Portal and ProtoGENI libraries
import geni.portal as portal
import geni.rspec.pg as pg

# Create a Portal context
pc = portal.Context()

# Create a Request object to start building the RSpec
request = pc.makeRequestRSpec()

# Define the node configuration
node = request.RawPC("gpu-node")
node.hardware_type = "d7525"  # Set to your GPU node type "d7525"

# Set the operating system image for the node
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD"  # Using Ubuntu 22.04

# Define a script to automatically install the deep learning environment at startup
setup_script = (
    "#!/bin/bash\n"
    "sudo apt-get update -y && "
    "sudo apt-get install -y build-essential gcc g++ make && "
    "sudo apt-get install -y python3.8 python3-pip python3.8-venv && "
    "sudo apt-get install -y nvidia-driver-510 && "
    "sudo apt-get install -y cuda-11-7 && "
    "sudo ln -s /usr/local/cuda-11.7 /usr/local/cuda && "
    "echo 'export PATH=/usr/local/cuda-11.7/bin:$PATH' >> ~/.bashrc && "
    "echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.7/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc && "
    "source ~/.bashrc && "
    "pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117 && "
    "pip3 install numpy scipy pandas matplotlib && "
    "python3.8 -m venv dl_env && "
    "source dl_env/bin/activate && pip install torch torchvision torchaudio numpy scipy pandas matplotlib && "
    "python3 -c \"import torch; print('CUDA available:', torch.cuda.is_available()); print('CUDA device count:', torch.cuda.device_count()); print('CUDA device name:', torch.cuda.get_device_name(0))\" && "
    "echo 'Deep learning environment installation completed'"
)

# Add the installation script as a service to the node
node.addService(pg.Execute(shell="bash", command=setup_script))

# Output the RSpec
pc.printRequestRSpec(request)
