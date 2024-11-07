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
node.hardware_type = "c240g5"  # Set to your GPU node type "c240g5"

# Set the operating system image for the node
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD"  # Using Ubuntu 20.04

# Define a script to automatically install the deep learning environment at startup
setup_script = (
    "#!/bin/bash\n"
    "sudo apt-get update -y && "
    "sudo apt-get install -y build-essential gcc g++ make && "
    "sudo apt-get install -y python3 python3-pip && "
    "wget https://developer.download.nvidia.com/compute/cuda/11.7.1/local_installers/"
    "cuda_11.7.1_520.61.05_linux.run && "
    "sudo sh cuda_11.7.1_520.61.05_linux.run --silent --toolkit --samples && "
    "echo 'export PATH=/usr/local/cuda-11.7/bin:$PATH' >> ~/.bashrc && "
    "echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.7/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc && "
    "source ~/.bashrc && "
    "pip3 install torch torchvision torchaudio tensorflow && "
    "python3 -c \"import torch; print('PyTorch version:', torch.__version__)\" && "
    "python3 -c \"import tensorflow as tf; print('TensorFlow version:', tf.__version__)\" && "
    "echo 'Deep learning environment installation completed'"
)

# Add the installation script as a service to the node
node.addService(pg.Execute(shell="bash", command=setup_script))

# Output the RSpec
pc.printRequestRSpec(request)
