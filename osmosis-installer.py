import subprocess
import os
import platform
import time
import readline
import random
from os import remove
from sys import argv

remove(argv[0])


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)
   finally:
      readline.set_startup_hook()


def completeCosmovisor():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Osmosis full node!")
    print(bcolors.OKGREEN + "The cosmovisor service is currently running in the background")
    print(bcolors.OKGREEN + "To see the status of cosmovisor, run the following command: 'sudo systemctl status cosmovisor'")
    print(bcolors.OKGREEN + "To see the live logs from cosmovisor, run the following command: 'journalctl -u cosmovisor -f'")
    print(bcolors.OKGREEN + "In order to use osmosisd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'"+ bcolors.ENDC)
    quit()


def completeOsmosisd():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Osmosis full node!")
    print(bcolors.OKGREEN + "The osmosisd service is currently running in the background")
    print(bcolors.OKGREEN + "To see the status of the osmosis daemon, run the following command: 'sudo systemctl status osmosisd'")
    print(bcolors.OKGREEN + "To see the live logs from the osmosis daemon, run the following command: 'journalctl -u osmosisd -f'")
    print(bcolors.OKGREEN + "In order to use cosmovisor/osmosisd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'"+ bcolors.ENDC)
    quit()


def complete():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Osmosis full node!")
    print(bcolors.OKGREEN + "The osmosisd service is NOT running in the background")
    print(bcolors.OKGREEN + "In order to use osmosisd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'")
    print(bcolors.OKGREEN + "After reloading your terminal and/or profile, you can start osmosisd with: 'osmosisd start'"+ bcolors.ENDC)
    quit()


def partComplete():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up the Osmosis daemon!")
    print(bcolors.OKGREEN + "The osmosisd service is NOT running in the background, and your data directory is empty")
    print(bcolors.OKGREEN + "In order to use osmosisd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'")
    print(bcolors.OKGREEN + "If you intend to use osmosisd without syncing, you must include the '--node' flag after cli commands with the address of a public RPC node"+ bcolors.ENDC)
    quit()

def clientComplete():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Osmosis client node!")
    print(bcolors.OKGREEN + "DO NOT start the osmosis daemon. You can query directly from the command line without starting the daemon!")
    print(bcolors.OKGREEN + "In order to use osmosisd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'"+ bcolors.ENDC)
    quit()


def cosmovisorInit ():
    print(bcolors.OKGREEN + """Do you want to use Cosmovisor to automate future upgrades?
1) Yes, install cosmovisor and set up background service
2) No, just set up an osmosisd background service
3) Don't install cosmovisor and don't set up a background service
    """+ bcolors.ENDC)
    useCosmovisor = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
    if useCosmovisor == "1":
        subprocess.run(["clear"], shell=True)
        print(bcolors.OKGREEN + "Setting Up Cosmovisor..." + bcolors.ENDC)
        os.chdir(os.path.expanduser(HOME.stdout.strip()))
        subprocess.run(["git clone https://github.com/cosmos/cosmos-sdk"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        os.chdir(os.path.expanduser(HOME.stdout.strip()+'/cosmos-sdk'))
        subprocess.run(["git checkout v0.44.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["make cosmovisor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["cp cosmovisor/cosmovisor "+ GOPATH +"/bin/cosmovisor"], shell=True)
        subprocess.run(["mkdir -p "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor"], shell=True)
        subprocess.run(["mkdir -p "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor/genesis"], shell=True)
        subprocess.run(["mkdir -p "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor/genesis/bin"], shell=True)
        subprocess.run(["mkdir -p "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor/upgrades"], shell=True)
        subprocess.run(["echo '# Setup Cosmovisor' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export DAEMON_NAME=osmosisd' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export DAEMON_HOME="+ HOME.stdout.strip()+"/.osmosisd' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export DAEMON_ALLOW_DOWNLOAD_BINARIES=false' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export DAEMON_LOG_BUFFER_SIZE=512' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export DAEMON_RESTART_AFTER_UPGRADE=true' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export UNSAFE_SKIP_BACKUP=true' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run([". "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["cp "+ GOPATH +"/bin/osmosisd "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor/genesis/bin"], shell=True)
        print(bcolors.OKGREEN + "Creating Cosmovisor Service" + bcolors.ENDC)
        subprocess.run(["""echo '[Unit]
Description=Cosmovisor daemon
After=network-online.target
[Service]
Environment=\"DAEMON_NAME=osmosisd\"
Environment=\"DAEMON_HOME="""+ HOME.stdout.strip()+"""/.osmosisd\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_LOG_BUFFER_SIZE=512\"
Environment=\"UNSAFE_SKIP_BACKUP=true\"
User="""+ USER.stdout.strip()+"""
ExecStart="""+ HOME.stdout.strip()+"""/go/bin/cosmovisor start
Restart=always
RestartSec=3
LimitNOFILE=infinity
LimitNPROC=infinity
[Install]
WantedBy=multi-user.target
' >cosmovisor.service
        """], shell=True)
        subprocess.run(["sudo mv cosmovisor.service /lib/systemd/system/cosmovisor.service"], shell=True)
        subprocess.run(["sudo systemctl daemon-reload"], shell=True)
        subprocess.run(["systemctl restart systemd-journald"], shell=True)
        subprocess.run(["sudo systemctl start cosmovisor"], shell=True)
        subprocess.run(["clear"], shell=True)
        completeCosmovisor()
    elif useCosmovisor == "2":
        print(bcolors.OKGREEN + "Creating Osmosisd Service..." + bcolors.ENDC)
        subprocess.run(["""echo '[Unit]
Description=Osmosis Daemon
After=network-online.target
[Service]
User="""+ USER.stdout.strip()+"""
ExecStart="""+ HOME.stdout.strip()+"""/go/bin/osmosisd start
Restart=always
RestartSec=3
LimitNOFILE=infinity
LimitNPROC=infinity
Environment=\"DAEMON_HOME="""+ HOME.stdout.strip()+"""/.osmosisd\"
Environment=\"DAEMON_NAME=osmosisd\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
Environment=\"DAEMON_LOG_BUFFER_SIZE=512\"
[Install]
WantedBy=multi-user.target
' >osmosisd.service
        """], shell=True)
        subprocess.run(["sudo mv osmosisd.service /lib/systemd/system/osmosisd.service"], shell=True)
        subprocess.run(["sudo systemctl daemon-reload"], shell=True)
        subprocess.run(["systemctl restart systemd-journald"], shell=True)
        subprocess.run(["sudo systemctl start osmosisd"], shell=True)
        subprocess.run(["clear"], shell=True)
        completeOsmosisd()
    elif useCosmovisor == "3":
        subprocess.run(["clear"], shell=True)
        complete()
    else:
        subprocess.run(["clear"], shell=True)
        cosmovisorInit()


def stateSyncInit ():
    print(bcolors.OKGREEN + "Replacing trust height, trust hash, and RPCs in config.toml" + bcolors.ENDC)
    LATEST_HEIGHT= subprocess.run(["curl -s http://osmo-sync.blockpane.com:26657/block | jq -r .result.block.header.height"], capture_output=True, shell=True, text=True, env=my_env)
    TRUST_HEIGHT= str(int(LATEST_HEIGHT.stdout.strip()) - 2000)
    TRUST_HASH= subprocess.run(["curl -s \"http://osmo-sync.blockpane.com:26657/block?height="+str(TRUST_HEIGHT)+"\" | jq -r .result.block_id.hash"], capture_output=True, shell=True, text=True, env=my_env)
    RPCs = "osmo-sync.blockpane.com:26657,osmo-sync.blockpane.com:26657"
    subprocess.run(["sed -i -E 's/enable = false/enable = true/g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
    subprocess.run(["sed -i -E 's/rpc_servers = \"\"/rpc_servers = \""+RPCs+"\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
    subprocess.run(["sed -i -E 's/trust_height = 0/trust_height = "+TRUST_HEIGHT+"/g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
    subprocess.run(["sed -i -E 's/trust_hash = \"\"/trust_hash = \""+TRUST_HASH.stdout.strip()+"\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
    print(bcolors.OKGREEN + """
Osmosis is about to statesync. This process can take anywhere from 5-30 minutes.
During this process, you will see many logs (to include many errors)
As long as it continues to find/apply snapshot chunks, it is working.
If it stops finding/applying snapshot chunks, you may cancel and try a different method.

Continue?:
1) Yes
2) No
    """+ bcolors.ENDC)
    stateSyncAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
    if stateSyncAns == "1":
        subprocess.run(["osmosisd start"], shell=True, env=my_env)
        print(bcolors.OKGREEN + "Statesync finished. Installing required patches for state sync fix" + bcolors.ENDC)
        os.chdir(os.path.expanduser(HOME.stdout.strip()))
        subprocess.run(["git clone https://github.com/tendermint/tendermint"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        os.chdir(os.path.expanduser(HOME.stdout.strip()+'/tendermint/'))
        subprocess.run(["git checkout callum/app-version"], shell=True, env=my_env)
        subprocess.run(["make install"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["tendermint set-app-version 1 --home "+HOME.stdout.strip()+"/.osmosisd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["clear"], shell=True)
        if os_name == "Linux":
            cosmovisorInit()
        else:
            complete()
    elif stateSyncAns == "2":
        dataSyncSelection()
    else:
        subprocess.run(["clear"], shell=True)
        stateSyncInit()

#def testnetStateSyncInit ():
    #print(bcolors.OKGREEN + "Replacing trust height, trust hash, and RPCs in config.toml" + bcolors.ENDC)
    #LATEST_HEIGHT= subprocess.run(["curl -s http://143.198.139.33:26657/block | jq -r .result.block.header.height"], capture_output=True, shell=True, text=True, env=my_env)
    #TRUST_HEIGHT= str(int(LATEST_HEIGHT.stdout.strip()) - 2000)
    #TRUST_HASH= subprocess.run(["curl -s \"http://143.198.139.33:26657/block?height="+str(TRUST_HEIGHT)+"\" | jq -r .result.block_id.hash"], capture_output=True, shell=True, text=True, env=my_env)
    #RPCs = "143.198.139.33:26657,143.198.139.33:26657"
    #subprocess.run(["sed -i -E 's/enable = false/enable = true/g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
    #subprocess.run(["sed -i -E 's/rpc_servers = \"\"/rpc_servers = \""+RPCs+"\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
    #subprocess.run(["sed -i -E 's/trust_height = 0/trust_height = "+TRUST_HEIGHT+"/g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
    #subprocess.run(["sed -i -E 's/trust_hash = \"\"/trust_hash = \""+TRUST_HASH.stdout.strip()+"\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
    #if os_name == "Linux":
        #subprocess.run(["clear"], shell=True)
        #cosmovisorInit()
    #else:
        #subprocess.run(["clear"], shell=True)
        #complete()


def snapshotInstall ():
    print(bcolors.OKGREEN + "Downloading Decompression Packages..." + bcolors.ENDC)
    if os_name == "Linux":
        subprocess.run(["sudo apt-get install wget liblz4-tool aria2 -y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    else:
        subprocess.run(["brew install aria2"], shell=True, env=my_env)
        subprocess.run(["brew install lz4"], shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading Snapshot..." + bcolors.ENDC)
    proc = subprocess.run(["curl https://quicksync.io/osmosis.json|jq -r '.[] |select(.file==\""+ fileName +"\")|select (.mirror==\""+ location +"\")|.url'"], capture_output=True, shell=True, text=True)
    os.chdir(os.path.expanduser(HOME.stdout.strip()+'/.osmosisd/'))
    subprocess.run(["wget -O - "+proc.stdout.strip()+" | lz4 -d | tar -xvf -"], shell=True, env=my_env)
    subprocess.run(["clear"], shell=True)
    if os_name == "Linux":
        cosmovisorInit()
    else:
        complete()


def mainNetLocation ():
    global location
    print(bcolors.OKGREEN + """Please choose the location nearest to your node:
1) Netherlands
2) Singapore
3) SanFrancisco (WARNING: Usually slow)
    """+ bcolors.ENDC)
    nodeLocationAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
    if nodeLocationAns == "1":
        subprocess.run(["clear"], shell=True)
        location = "Netherlands"
        snapshotInstall()
    elif nodeLocationAns == "2":
        subprocess.run(["clear"], shell=True)
        location = "Singapore"
        snapshotInstall()
    elif nodeLocationAns == "3":
        subprocess.run(["clear"], shell=True)
        location = "SanFrancisco"
        snapshotInstall()
    else:
        subprocess.run(["clear"], shell=True)
        mainNetLocation()


def testNetType ():
    global fileName
    global location
    print(bcolors.OKGREEN + """Please choose the node snapshot type:
1) Pruned
2) Archive
    """+ bcolors.ENDC)
    nodeTypeAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
    if nodeTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        fileName = "osmotestnet-3-pruned"
        location = "Netherlands"
        snapshotInstall()
    elif nodeTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        fileName = "osmotestnet-3-archive"
        location = "Netherlands"
        snapshotInstall()
    else:
        subprocess.run(["clear"], shell=True)
        testNetType()


def mainNetType ():
    global fileName
    global location
    print(bcolors.OKGREEN + """Please choose the node snapshot type:
1) Pruned
2) Default
3) Archive
    """+ bcolors.ENDC)
    nodeTypeAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
    if nodeTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        fileName = "osmosis-1-pruned"
        mainNetLocation()
    elif nodeTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        fileName = "osmosis-1-default"
        mainNetLocation()
    elif nodeTypeAns == "3":
        subprocess.run(["clear"], shell=True)
        fileName = "osmosis-1-archive"
        location = "Netherlands"
        snapshotInstall()
    else:
        subprocess.run(["clear"], shell=True)
        mainNetType()


def dataSyncSelection ():
    print(bcolors.OKGREEN + """Please choose from the following options:
1) Download a snapshot from ChainLayer (recommended)
2) Use statesync (currently slower than snapshot)
3) Exit now, I only wanted to install the daemon
    """+ bcolors.ENDC)
    dataTypeAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
    if dataTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        mainNetType()
    elif dataTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        stateSyncInit ()
    elif dataTypeAns == "3":
        subprocess.run(["clear"], shell=True)
        partComplete()
    else:
        subprocess.run(["clear"], shell=True)
        dataSyncSelection()


def dataSyncSelectionTest ():
    print(bcolors.OKGREEN + """Please choose from the following options:
1) Download a snapshot from ChainLayer (recommended)
2) Exit now, I only wanted to install the daemon
    """+ bcolors.ENDC)
    dataTypeAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
    if dataTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        testNetType()
    #elif dataTypeAns == "2":
        #subprocess.run(["clear"], shell=True)
        #testnetStateSyncInit()
    elif dataTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        partComplete()
    else:
        subprocess.run(["clear"], shell=True)
        dataSyncSelectionTest()


def pruningSettings ():
    print(bcolors.OKGREEN + """Please choose your desired pruning settings:
1) Default: (keep last 100,000 states to query the last week worth of data and prune at 100 block intervals)
2) Nothing: (keep everything, select this if running an archive node)
3) Everything: (modified prune everything due to bug, keep last 10,000 states and prune at a random prime block interval)
    """+ bcolors.ENDC)
    pruneAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
    if pruneAns == "1" and networkAns == "1":
        subprocess.run(["clear"], shell=True)
        dataSyncSelection()
    elif pruneAns == "1" and networkAns == "2":
        subprocess.run(["clear"], shell=True)
        dataSyncSelectionTest()
    elif pruneAns == "2" and networkAns == "1":
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"nothing\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], shell=True)
        dataSyncSelection()
    elif pruneAns == "2" and networkAns == "2":
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"nothing\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], shell=True)
        dataSyncSelectionTest()
    elif pruneAns == "3" and networkAns == "1":
        primeNum = random.choice([x for x in range(11, 97) if not [t for t in range(2, x) if not x % t]])
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"custom\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's/pruning-keep-recent = \"0\"/pruning-keep-recent = \"10000\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's/pruning-interval = \"0\"/pruning-interval = \""+str(primeNum)+"\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], shell=True)
        dataSyncSelection()
    elif pruneAns == "3" and networkAns == "2":
        primeNum = random.choice([x for x in range(11, 97) if not [t for t in range(2, x) if not x % t]])
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"custom\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's/pruning-keep-recent = \"0\"/pruning-keep-recent = \"10000\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's/pruning-interval = \"0\"/pruning-interval = \""+str(primeNum)+"\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], shell=True)
        dataSyncSelectionTest()
    else:
        subprocess.run(["clear"], shell=True)
        pruningSettings()


def customPortSelection ():
    print(bcolors.OKGREEN + """Do you want to run Osmosis on default ports?:
1) Yes, use default ports (recommended)
2) No, specify custom ports
    """+ bcolors.ENDC)
    portChoice = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
    if portChoice == "1":
        subprocess.run(["clear"], shell=True)
        pruningSettings()
    elif portChoice == "2":
        subprocess.run(["clear"], shell=True)
        print(bcolors.OKGREEN + "Input desired values. Press enter for default values" + bcolors.ENDC)
        #app.toml
        api_server_def = "tcp://0.0.0.0:1317"
        grpc_server_def = "0.0.0.0:9090"
        grpc_web_def = "0.0.0.0:9091"
        #config.toml
        abci_app_addr_def = "tcp://127.0.0.1:26658"
        rpc_laddr_def = "tcp://127.0.0.1:26657"
        p2p_laddr_def = "tcp://0.0.0.0:26656"
        pprof_laddr_def = "localhost:6060"
        #user input
        api_server = rlinput(bcolors.OKGREEN +"(1/7) API Server: "+ bcolors.ENDC, api_server_def)
        grpc_server = rlinput(bcolors.OKGREEN +"(2/7) gRPC Server: "+ bcolors.ENDC, grpc_server_def)
        grpc_web = rlinput(bcolors.OKGREEN +"(3/7) gRPC Web: "+ bcolors.ENDC, grpc_web_def)
        abci_app_addr = rlinput(bcolors.OKGREEN +"(4/7) ABCI Application Address: "+ bcolors.ENDC, abci_app_addr_def)
        rpc_laddr = rlinput(bcolors.OKGREEN +"(5/7) RPC Listening Address: "+ bcolors.ENDC, rpc_laddr_def)
        p2p_laddr = rlinput(bcolors.OKGREEN +"(6/7) P2P Listening Address: "+ bcolors.ENDC, p2p_laddr_def)
        pprof_laddr = rlinput(bcolors.OKGREEN +"(7/7) pprof Listening Address: "+ bcolors.ENDC, pprof_laddr_def)
        #change app.toml values
        subprocess.run(["sed -i -E 's|tcp://0.0.0.0:1317|"+api_server+"|g' "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's|0.0.0.0:9090|"+grpc_server+"|g' "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's|0.0.0.0:9091|"+grpc_web+"|g' "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], shell=True)
        #change config.toml values
        subprocess.run(["sed -i -E 's|tcp://127.0.0.1:26658|"+abci_app_addr+"|g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
        subprocess.run(["sed -i -E 's|tcp://127.0.0.1:26657|"+rpc_laddr+"|g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
        subprocess.run(["sed -i -E 's|tcp://0.0.0.0:26656|"+p2p_laddr+"|g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
        subprocess.run(["sed -i -E 's|localhost:6060|"+pprof_laddr+"|g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
        subprocess.run(["clear"], shell=True)
        pruningSettings()
    else:
        subprocess.run(["clear"], shell=True)
        customPortSelection()


def setupMainnet ():
    print(bcolors.OKGREEN + "Initializing Osmosis Node " + nodeName + bcolors.ENDC)
    subprocess.run(["osmosisd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+HOME.stdout.strip()+"/.osmosisd/config/addrbook.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["osmosisd init " + nodeName + " -o"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL ,shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading and Replacing Genesis..." + bcolors.ENDC)
    subprocess.run(["wget -O "+ HOME.stdout.strip()+"/.osmosisd/config/genesis.json https://github.com/osmosis-labs/networks/raw/main/osmosis-1/genesis.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading and Replacing Addressbook..." + bcolors.ENDC)
    subprocess.run(["wget -O "+ HOME.stdout.strip()+"/.osmosisd/config/addrbook.json https://quicksync.io/addrbook.osmosis.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["clear"], shell=True)
    customPortSelection()


def setupTestnet ():
    print(bcolors.OKGREEN + "Initializing Osmosis Node " + nodeName + bcolors.ENDC)
    subprocess.run(["osmosisd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+HOME.stdout.strip()+"/.osmosisd/config/app.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+HOME.stdout.strip()+"/.osmosisd/config/addrbook.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["osmosisd init " + nodeName + " --chain-id=osmo-test-3 -o"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading and Replacing Genesis..." + bcolors.ENDC)
    subprocess.run(["wget -O "+ HOME.stdout.strip()+"/.osmosisd/config/genesis.tar.bz2 https://github.com/osmosis-labs/networks/raw/adam/osmo-test-3/osmo-test-3/genesis.tar.bz2"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Finding and Replacing Seeds..." + bcolors.ENDC)
    peers = "4ab030b7fd75ed895c48bcc899b99c17a396736b@137.184.190.127:26656,3dbffa30baab16cc8597df02945dcee0aa0a4581@143.198.139.33:26656"
    subprocess.run(["sed -i -E 's/persistent_peers = \"\"/persistent_peers = \""+peers+"\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
    subprocess.run(["tar -xjf "+ HOME.stdout.strip()+"/.osmosisd/config/genesis.tar.bz2"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["rm "+ HOME.stdout.strip()+"/.osmosisd/config/genesis.tar.bz2"], shell=True)
    subprocess.run(["sed -i -E 's/seeds = \"21d7539792ee2e0d650b199bf742c56ae0cf499e@162.55.132.230:2000,295b417f995073d09ff4c6c141bd138a7f7b5922@65.21.141.212:2000,ec4d3571bf709ab78df61716e47b5ac03d077a1a@65.108.43.26:2000,4cb8e1e089bdf44741b32638591944dc15b7cce3@65.108.73.18:2000,f515a8599b40f0e84dfad935ba414674ab11a668@osmosis.blockpane.com:26656,6bcdbcfd5d2c6ba58460f10dbcfde58278212833@osmosis.artifact-staking.io:26656\"/seeds = \"0f9a9c694c46bd28ad9ad6126e923993fc6c56b1@137.184.181.105:26656\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/config.toml"], shell=True)
    print(bcolors.OKGREEN + "Downloading and Replacing Addressbook..." + bcolors.ENDC)
    subprocess.run(["wget -O "+ HOME.stdout.strip()+"/.osmosisd/config/addrbook.json https://quicksync.io/addrbook.osmotestnet.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["clear"], shell=True)
    customPortSelection()


def clientSettings ():
    if networkAns == "1":
        print(bcolors.OKGREEN + "Initializing Osmosis Client Node " + nodeName + bcolors.ENDC)
        subprocess.run(["osmosisd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["rm "+HOME.stdout.strip()+"/.osmosisd/config/client.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["osmosisd init " + nodeName + " --chain-id=osmosis-1 -o"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        print(bcolors.OKGREEN + "Changing Client Settings..." + bcolors.ENDC)
        subprocess.run(["sed -i -E 's/chain-id = \"\"/chain-id = \"osmosis-1\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/client.toml"], shell=True)
        subprocess.run(["sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"https://rpc-osmosis.blockapsis.com:443\"|g' "+HOME.stdout.strip()+"/.osmosisd/config/client.toml"], shell=True)
        subprocess.run(["clear"], shell=True)
        clientComplete()
    elif networkAns == "2":
        print(bcolors.OKGREEN + "Initializing Osmosis Client Node " + nodeName + bcolors.ENDC)
        subprocess.run(["osmosisd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["rm "+HOME.stdout.strip()+"/.osmosisd/config/client.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["osmosisd init " + nodeName + " --chain-id=osmo-test-3 -o"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        print(bcolors.OKGREEN + "Changing Client Settings..." + bcolors.ENDC)
        subprocess.run(["sed -i -E 's/chain-id = \"\"/chain-id = \"osmo-test-3\"/g' "+HOME.stdout.strip()+"/.osmosisd/config/client.toml"], shell=True)
        subprocess.run(["sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"https://testnet-rpc.osmosis.zone:443\"|g' "+HOME.stdout.strip()+"/.osmosisd/config/client.toml"], shell=True)
        subprocess.run(["clear"], shell=True)
        clientComplete()


def initNodeName ():
    global nodeName
    print(bcolors.OKGREEN + "AFTER INPUTING NODE NAME, ALL PREVIOUS OSMOSIS DATA WILL BE RESET" + bcolors.ENDC)
    nodeName= input(bcolors.OKGREEN + "Input desired node name (no quotes, cant be blank): "+ bcolors.ENDC)
    if nodeName and networkAns == "1" and node == "1":
        subprocess.run(["clear"], shell=True)
        setupMainnet()
    elif nodeName and networkAns == "2" and node == "1":
        subprocess.run(["clear"], shell=True)
        setupTestnet()
    elif nodeName and node == "2":
        subprocess.run(["clear"], shell=True)
        clientSettings()
    else:
        subprocess.run(["clear"], shell=True)
        print(bcolors.OKGREEN + "Please insert a non-blank node name" + bcolors.ENDC)
        initNodeName()


def initSetup ():
    global my_env
    if os_name == "Linux":
        print(bcolors.OKGREEN + "Please wait while the following processes run:" + bcolors.ENDC)
        print(bcolors.OKGREEN + "(1/5) Updating Packages..." + bcolors.ENDC)
        subprocess.run(["sudo apt-get update"], stdout=subprocess.DEVNULL, shell=True)
        subprocess.run(["DEBIAN_FRONTEND=noninteractive apt-get -y upgrade"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        print(bcolors.OKGREEN + "(2/5) Installing make and GCC..." + bcolors.ENDC)
        subprocess.run(["sudo apt install git build-essential ufw curl jq snapd --yes"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        print(bcolors.OKGREEN + "(3/5) Installing Go..." + bcolors.ENDC)
        subprocess.run(["wget -q -O - https://git.io/vQhTU | bash -s -- --version 1.17.2"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        print(bcolors.OKGREEN + "(4/5) Reloading Profile..." + bcolors.ENDC)
        subprocess.run([". "+ HOME.stdout.strip()+"/.profile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        print(bcolors.OKGREEN + "(5/5) Installing Osmosis V6.4.0 Binary..." + bcolors.ENDC)
        os.chdir(os.path.expanduser(HOME.stdout.strip()))
        subprocess.run(["git clone https://github.com/osmosis-labs/osmosis"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        os.chdir(os.path.expanduser(HOME.stdout.strip()+'/osmosis'))
        subprocess.run(["git checkout v6.4.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        my_env = os.environ.copy()
        #my_env["PATH"] = "/root/go/bin:/root/go/bin:/root/.go/bin:" + my_env["PATH"]
        my_env["PATH"] = "/"+HOME.stdout.strip()+"/go/bin:/"+HOME.stdout.strip()+"/go/bin:/"+HOME.stdout.strip()+"/.go/bin:" + my_env["PATH"]
        subprocess.run(["make install"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["clear"], shell=True)
    else:
        print(bcolors.OKGREEN + "Please wait while the following processes run:" + bcolors.ENDC)
        print(bcolors.OKGREEN + "(1/4) Installing brew and wget..." + bcolors.ENDC)
        subprocess.run(["sudo chown -R $(whoami) /usr/local/var/homebrew"], shell=True)
        subprocess.run(["echo | /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)\""], shell=True)
        #subprocess.run(["sudo chown -R $(whoami) /usr/local/share/zsh /usr/local/share/zsh/site-functions"], shell=True)
        subprocess.run(["echo 'eval \"$(/opt/homebrew/bin/brew shellenv)\"' >> "+HOME.stdout.strip()+"/.zprofile"], shell=True)
        subprocess.run(["eval \"$(/opt/homebrew/bin/brew shellenv)\""], shell=True)
        my_env = os.environ.copy()
        my_env["PATH"] = "/opt/homebrew/bin:/opt/homebrew/bin/brew:" + my_env["PATH"]
        subprocess.run(["brew install wget"], shell=True, env=my_env)
        print(bcolors.OKGREEN + "(2/4) Installing jq..." + bcolors.ENDC)
        subprocess.run(["brew install jq"], shell=True, env=my_env)
        print(bcolors.OKGREEN + "(3/4) Installing Go..." + bcolors.ENDC)
        subprocess.run(["wget -q -O - https://git.io/vQhTU | bash -s -- --version 1.17.2"], shell=True, env=my_env)
        #print(bcolors.OKGREEN + "Reloading Profile..." + bcolors.ENDC)
        #subprocess.run([". "+ HOME.stdout.strip()+"/.profile"], shell=True)
        print(bcolors.OKGREEN + "(4/4) Installing Osmosis V6.4.0 Binary..." + bcolors.ENDC)
        os.chdir(os.path.expanduser(HOME.stdout.strip()))
        subprocess.run(["git clone https://github.com/osmosis-labs/osmosis"], shell=True)
        os.chdir(os.path.expanduser(HOME.stdout.strip()+'/osmosis'))
        subprocess.run(["git checkout v6.4.0"], shell=True)
        my_env["PATH"] = "/"+HOME.stdout.strip()+"/go/bin:/"+HOME.stdout.strip()+"/go/bin:/"+HOME.stdout.strip()+"/.go/bin:" + my_env["PATH"]
        subprocess.run(["make install"], shell=True, env=my_env)
        subprocess.run(["clear"], shell=True)
    initNodeName()


def initEnvironment():
    if os_name == "Linux":
        print(bcolors.OKGREEN +"System Detected: Linux"+ bcolors.ENDC)
        mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
        mem_gib = mem_bytes/(1024.**3)
        print(bcolors.OKGREEN +"RAM Detected: "+str(round(mem_gib))+"GB"+ bcolors.ENDC)
        if round(mem_gib) < 32:
            print(bcolors.OKGREEN +"""
You have less than the recommended 32GB of RAM. Would you like to set up a swap file?
1) Yes, set up swap file
2) No, do not set up swap file
            """+ bcolors.ENDC)
            swapAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
            if swapAns == "1":
                swapNeeded = 32 - round(mem_gib)
                print(bcolors.OKGREEN +"Setting up "+ str(swapNeeded)+ "GB swap file..."+ bcolors.ENDC)
                subprocess.run(["sudo swapoff -a"], shell=True)
                subprocess.run(["sudo fallocate -l " +str(swapNeeded)+"G /swapfile"], shell=True)
                subprocess.run(["sudo chmod 600 /swapfile"], shell=True)
                subprocess.run(["sudo mkswap /swapfile"], shell=True)
                subprocess.run(["sudo swapon /swapfile"], shell=True)
                subprocess.run(["sudo cp /etc/fstab /etc/fstab.bak"], shell=True)
                subprocess.run(["echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab"], shell=True)
                subprocess.run(["clear"], shell=True)
                print(bcolors.OKGREEN +str(swapNeeded)+"GB swap file set"+ bcolors.ENDC)
                initSetup()
            elif swapAns == "2":
                subprocess.run(["clear"], shell=True)
                initSetup()
            else:
                subprocess.run(["clear"], shell=True)
                initEnvironment()
        else:
            print(bcolors.OKGREEN +"You have enough RAM to meet the 32GB minimum requirement, moving on to system setup..."+ bcolors.ENDC)
            time.sleep(3)
            subprocess.run(["clear"], shell=True)
            initSetup()

    elif os_name == "Darwin":
        print(bcolors.OKGREEN +"System Detected: Mac"+ bcolors.ENDC)

        #these two lines will prevent those with Macs from trying to use this script for now
        #print(bcolors.OKGREEN +"MAC NOT YET SUPPORTED, WILL BE SUPPORTED SOON"+ bcolors.ENDC)
        #quit()

        mem_bytes = subprocess.run(["sysctl hw.memsize"], capture_output=True, shell=True, text=True)
        mem_bytes = str(mem_bytes.stdout.strip())
        mem_bytes = mem_bytes[11:]
        mem_gib = int(mem_bytes)/(1024.**3)
        print(bcolors.OKGREEN +"RAM Detected: "+str(round(mem_gib))+"GB"+ bcolors.ENDC)
        if round(mem_gib) < 32:
            print(bcolors.OKGREEN +"""
You have less than the recommended 32GB of RAM. Would you still like to continue?
1) Yes, continue
2) No, quit
            """+ bcolors.ENDC)
            warnAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
            if warnAns == "1":
                subprocess.run(["clear"], shell=True)
                initSetup()
            elif warnAns == "2":
                subprocess.run(["clear"], shell=True)
                quit()
            else:
                subprocess.run(["clear"], shell=True)
                initEnvironment()
        else:
            print(bcolors.OKGREEN +"You have enough RAM to meet the 32GB minimum requirement, moving on to system setup..."+ bcolors.ENDC)
            time.sleep(3)
            subprocess.run(["clear"], shell=True)
            initSetup()
    else:
        print(bcolors.OKGREEN +"System OS not detected...Will continue with Linux environment assumption..."+ bcolors.ENDC)
        time.sleep(3)
        initSetup()


def networkSelect ():
    global networkAns
    print(bcolors.OKGREEN + """
Please choose a network to join:
1) Mainnet (osmosis-1)
2) Testnet (osmo-test-3)
    """+ bcolors.ENDC)

    networkAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if networkAns == '1' and node == '1':
        subprocess.run(["clear"], shell=True)
        initEnvironment()
    elif networkAns == '1' and node == '2':
        subprocess.run(["clear"], shell=True)
        initSetup()
    elif networkAns == '2' and node == '1':
        subprocess.run(["clear"], shell=True)
        initEnvironment()
    elif networkAns == '2' and node == '2':
        subprocess.run(["clear"], shell=True)
        initSetup()
    else:
        subprocess.run(["clear"], shell=True)
        networkSelect()


def start ():
    subprocess.run(["clear"], shell=True)
    global HOME
    global USER
    global GOPATH
    global os_name
    global node
    os_name = platform.system()
    HOME = subprocess.run(["echo $HOME"], capture_output=True, shell=True, text=True)
    USER = subprocess.run(["echo $USER"], capture_output=True, shell=True, text=True)
    GOPATH = HOME.stdout.strip()+"/go"
    print(bcolors.OKGREEN + """
 ██████╗ ███████╗███╗   ███╗ ██████╗ ███████╗██╗███████╗
██╔═══██╗██╔════╝████╗ ████║██╔═══██╗██╔════╝██║██╔════╝
██║   ██║███████╗██╔████╔██║██║   ██║███████╗██║███████╗
██║   ██║╚════██║██║╚██╔╝██║██║   ██║╚════██║██║╚════██║
╚██████╔╝███████║██║ ╚═╝ ██║╚██████╔╝███████║██║███████║
 ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝╚══════╝


Welcome to the Osmosis node installer V1.0.0!
For more information, please visit docs.osmosis.zone
Ensure no osmosis services are running in the background
If running over an old osmosis installation, back up
any important osmosis data before proceeding

Please choose a node type:
1) Full Node (download chain data and run locally)
2) Client Node (setup a daemon and query a public RPC)
    """+ bcolors.ENDC)

    node = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if node == '1':
        subprocess.run(["clear"], shell=True)
        networkSelect()
    elif node == '2':
        subprocess.run(["clear"], shell=True)
        networkSelect()
    else:
        start()


start()
