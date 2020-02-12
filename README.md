# etcd_scan
> Dump etcd Data

etcd is a distributed key-value store for most critical data of a distributed system.

Many open etcd ports without authentication are open to the internet.
You can find interesting data such as private keys, passwords, etc.

> Donate: (ETH) 0x489B56bA505F88a054893d5BdE2c8b35f4A33FAb

# Installation

```
git clone https://github.com/Ibonok/etcd_scan.git
cd etcd_scan

virtualenv .
source bin/activate
pip install -r requirements.txt
```
# Usage

```
python etcd_scan.py --help                 
usage: etcd_scan.py [-h] [-i [INFO]] [-d [DUMP]] [-o [OUTPUT]] [--ip [IP]] [-f [FILENAME]]

Dump etcd data. Default port 2379 hardcoded!

optional arguments:
  -h, --help            show this help message and exit
  -i [INFO], --info [INFO]
                        Only show metadata, Default = True
  -d [DUMP], --dump [DUMP]
                        Dump all data. Default = False
  -o [OUTPUT], --output [OUTPUT]
                        Output File: out/ip, json, Default = False
  --ip [IP]             Target IP:PORT
  -f [FILENAME], --filename [FILENAME]
                        File with IP:PORT
```

# Example
> Connect to etcd and get all data

```
➜  ~ python etcd_scan.py --ip 127.0.0.1 -d
#################### Metadata for 127.0.0.1 ####################

etcd Server Version:	3.3.2
etcd Cluster Version:	3.3.0

Name:		 localhost0001
peerURLs:	 ['http://127.0.0.1:2380']
clientURLs:	 ['http://127.0.0.1:2379']

#################### Data  ####################
{
  "action": "get",
  "node": {
    "dir": true,
    "nodes": [
      {
        "key": "/coreos.com",
        "dir": true,
        "nodes": [
          {
            "key": "/coreos.com/network",
            "dir": true,
            "nodes": [
              {
                "key": "/coreos.com/network/config",
                "value": "{\n  \"Backend\": {\n    \"Port\": 8285,\n    \"Type\": \"udp\"\n  },\n  \"Network\": \"10.2.0.0/16\",\n  \"SubnetLen\": 24,\n  \"SubnetMax\": \"10.2.255.0\",\n  \"SubnetMin\": \"10.2.0.0\"\n}",
                "modifiedIndex": 8,
                "createdIndex": 8
```

> Only get Metadata
```
python etcd_scan.py --ip 127.0.0.1
#################### Metadata for 127.0.0.1 ####################

etcd Server Version:	3.3.2
etcd Cluster Version:	3.3.0

Name:		 localhost0001
peerURLs:	 ['http://127.0.0.1:2380']
clientURLs:	 ['http://127.0.0.1:2379']
```

# Secure etcd

It is important that etcd instances must be securely configured.
You can find a guide on the github page of etcd.

https://github.com/etcd-io/etcd/blob/master/Documentation/op-guide/security.md

Further restrict the port to the system with a firewall or iptables.