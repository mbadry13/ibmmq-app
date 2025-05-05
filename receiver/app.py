import pymqi
import time

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

print("Connected to IBM MQ. Starting to receive messages...\n")

# Prepare options
gmo = pymqi.GMO()
gmo.Options = pymqi.CMQC.MQGMO_NO_WAIT | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING

try:
    while True:
        try:
            md = pymqi.MD()
            message = queue.get(None, md, gmo)
            print(f"[{time.strftime('%H:%M:%S')}] Received message: {message.decode()}")
        except pymqi.MQMIError as e:
            if e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
                print(f"[{time.strftime('%H:%M:%S')}] No messages available.")
            else:
                raise

        time.sleep(10)

except KeyboardInterrupt:
    print("\nInterrupted by user. Exiting...")

finally:
    try:
        queue.close()
    except pymqi.PYIFError:
        pass

    qmgr.disconnect()
    print("Disconnected from MQ.")

