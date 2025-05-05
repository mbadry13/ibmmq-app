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

conn_info = f'{host}({port})'

# Connect to MQ
qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)
queue = pymqi.Queue(qmgr, queue_name)

print("Connected to IBM MQ. Starting message loop...\n")

try:
    while True:
        # Generate random message
        random_message = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        full_message = f"Random Msg: {random_message}"

        # Put message on the queue
        queue.put(full_message)
        print(f"[{time.strftime('%H:%M:%S')}] Sent message: {full_message}")

        # Wait 30 seconds
        time.sleep(30)

except KeyboardInterrupt:
    print("\nInterrupted by user. Exiting...")

finally:
    # Cleanup
    queue.close()
    qmgr.disconnect()
    print("Disconnected from MQ.")

