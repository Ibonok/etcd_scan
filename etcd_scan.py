#!/usr/bin/python3
############
# @Author Ibonok
#
# Dump etcd keys
#
# Do not use this in productiv enviroments.
# For educational use only. 
# 
############ 
import requests
import os, errno, sys, argparse
import json
from pprint import pprint
from colorama import init, Fore, Style

def check_args ():
    init(autoreset=True)
    pars = argparse.ArgumentParser(description=Fore.GREEN + Style.BRIGHT + 'Dump etcd data. Default port 2379 hardcoded!' + Style.RESET_ALL)

    pars.add_argument('-i', '--info', type=bool, nargs='?', default=True, const=False, help='Only show metadata, Default = True')
    pars.add_argument('-d', '--dump', type=bool, nargs='?', default=False, const=True, help='Dump all data. Default = False')
    pars.add_argument('-o', '--output', type=bool, nargs='?', default=False, const=True, help='Output File: out/ip, json, Default = False')

    pars.add_argument('--ip', nargs='?', help='Target IP:PORT')
    pars.add_argument('-f', '--filename', nargs='?', help='File with IP:PORT')

    args = pars.parse_args()

    if args.ip is None and args.filename is None:
        pars.error(Fore.RED + '-f/--filename or --ip required')        
    elif args.ip and args.filename is None: 
        return args.ip, True, args.info, args.dump, args.output
    elif args.ip is None and args.filename: 
        return args.filename, False, args.info, args.dump, args.output
    elif args.ip and args.filename: 
        pars.error(Fore.RED + 'To many Parameters, please choose -f/--filename or --ip')

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def getMetadata(ip, port, output):
    print (Fore.GREEN + '#' * 20 + ' Metadata for ' + ip + ' ' + '#' * 20 + Style.RESET_ALL)
    print ('\r')
    r = requests.get('http://' + ip + ':2379/version')
    if r.status_code == 200:
        if output:
            write_json(ip, r.json())
        else:
            #print (json.dumps(r.json(), indent=2))
            print ("etcd Server Version:\t" + r.json()['etcdserver'])
            print ("etcd Cluster Version:\t" +r.json()['etcdcluster'])
            print ('\r')

    r = requests.get('http://' + ip + ':2379/v2/members')
    if r.status_code == 200: 
        if output:
            write_json(ip, r.json())
        else:
            for i in r.json()['members']:
                print ('Name:\t\t ' + i['name'])
                print ('peerURLs:\t', i['peerURLs'])
                print ('clientURLs:\t', i['clientURLs'])

def getData(ip, port, output):
    r = requests.get('http://' + ip + ':2379/v2/keys/?recursive=true')
    if r.status_code == 200:
        if output:
            write_json(ip, r.json())
        else:
            print (Fore.GREEN + '#' * 20 + ' Data  ' + '#' * 20 + Style.RESET_ALL)
            print (json.dumps(r.json(), indent=2))
            print ('\n')

def single_ip(ip, info, dump, output):
    if info:
        getMetadata(ip.rstrip(), 2379, output)
        print ('\n')
    if dump:
        getData(ip.rstrip(), 2379, output)

def input_file(filename, info, dump, output):
    file = open (filename, 'r')
    for ip in file:
        if info:
            getMetadata(ip.rstrip(), 2379, output)
        if dump:
            getData(ip.rstrip(), 2379, output)

def write_json(ip, data):
    try: 
        if os.path.exists("out") == False:
            os.makedirs('out')
        os.makedirs('out/')
    except OSError as e:
        if e.errno != errno.EEXIST:
            print (Fore.RED + 'Cannot create directory')
            raise
    
    try:
        if not os.path.exists('out/' + ip + '.json'):
            print (Fore.RED + 'Output to JSON filename: out' + Fore.GREEN + '/' + ip + '.json' + Style.RESET_ALL) 
        datei = open('out/' + ip + '.json', 'a')
        datei.write(json.dumps(data, indent=2))
        datei.write('\n')
        datei.close()
    except FileNotFoundError:
        print(Fore.RED + 'Input file not found!')

if __name__ == "__main__":
    try:
        (value, typ, info, dump, output) = check_args()
        if typ:
            single_ip(value, info, dump, output)
        else:
            input_file(value, info, dump, output)
    except KeyboardInterrupt:
        sys.exit()
