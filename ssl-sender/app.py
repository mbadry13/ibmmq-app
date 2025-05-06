import pymqi
import time
import random
import string

# MQ connection parameters
queue_manager = 'QM1'
channel = 'CHANNEL1'
host = '192.168.18.124'
port = '1414'
queue_name = 'MY.QUEUE.1'
user = 'mqm'
password = 'P@ssw0rd'

# SSL parameters
cipher_spec = 'TLS_AES_128_GCM_SHA256'  # Must match the server side

key_repo_location = '/app/ssl/client'         # Path to the .kdb/.sth files

conn_info = f'{host}({port})'

# Set MQ environment with SSL configuration
cd = pymqi.CD()
cd.ChannelName = channel.encode('utf-8')
cd.ConnectionName = conn_info.encode('utf-8')
cd.ChannelType = pymqi.CMQC.MQCHT_CLNTCONN
cd.TransportType = pymqi.CMQC.MQXPT_TCP
cd.SSLCipherSpec = cipher_spec.encode('utf-8')

sco = pymqi.SCO()
#sco.KeyRepository = key_repo_location
sco.KeyRepository = key_repo_location.encode('utf-8')


# Connect using CD and SCO objects for SSL
qmgr = pymqi.QueueManager(None)
qmgr.connect_with_options(queue_manager, user=user, password=password, cd=cd, sco=sco)
queue = pymqi.Queue(qmgr, queue_name)

print("Connected to IBM MQ over SSL. Starting message loop...\n")

try:
    while True:
        random_message = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        full_message = f"Random Msg: {random_message}"
        queue.put(full_message)
        print(f"[{time.strftime('%H:%M:%S')}] Sent message: {full_message}")
        time.sleep(30)

except KeyboardInterrupt:
    print("\nInterrupted by user. Exiting...")

finally:
    queue.close()
    qmgr.disconnect()
    print("Disconnected from MQ.")

