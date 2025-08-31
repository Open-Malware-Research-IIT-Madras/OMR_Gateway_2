import subprocess
import pika
import json
import os
import time
import uuid
import psycopg2
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='GATEWAY_2: %(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    filemode='w',
    filename='/var/log/omr/omr_webapp_gw2_logs.log'
)
logger = logging.getLogger(__name__)
logger.info('initializing connections to RabbitMQ and PostgreSQL')

credentials=pika.PlainCredentials('OMR_RMQ','Omr@123')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.5.1', 5672,'/', credentials))
connection2 = pika.BlockingConnection(pika.ConnectionParameters('192.168.5.1', 5672,'/', credentials))

#connection1 = psycopg2.connect(
 #                     database="omrdatabase",
  #                    host="172.23.254.74",
   #                   port=5432,
    #                  user="omruser",
     #                 password="Omr@123" ,
      #              )
#cursor=connection1.cursor()
#connection1.autocommit=True

def copyMalwareToGW1(filehash, jobid):
    script_path = "/home/omr/jugaad_file_transfer/shellScripts/copyMalware.sh"
    try:
        copy_call_with_args="/home/omr/jugaad_file_transfer/shellScripts/copyMalware.sh '%s'" % (str(filehash+".dat"))
        print("File copy executed form gateway2 to gateway1 start")
        os.system(copy_call_with_args)
        print('File copy executed form gateway2 to gateway1 end')

    except subprocess.CalledProcessError as e:
        print("error in copying the malware", e)
        logger.error(f'[{jobid}] : Error in copying malware to Gateway 1 {e}')

def run_remote_python(remote_host, remote_user, remote_directory, remote_python_script, python_arg, jobid):
    print("Called the remote python function with arguments \n\n",remote_host,remote_user, remote_directory,remote_python_script,python_arg)
    logger.info(f'[{jobid}] : Called the remote Python function on Gateway1 with args : {remote_host} - {remote_user} - {remote_directory} - {remote_python_script} - {python_arg}')
    copy_call_with_args="/home/omr/jugaad_file_transfer/shellScripts/runStartTesh.sh '%s' '%s' '%s' '%s' '%s'" % (str(remote_host),str(remote_user),str(remote_directory),str(remote_python_script),str(python_arg+".dat"))
    print("remote script invocation form Gateway1 to profiler callstart")
    logger.info(f'[{jobid}] : Remote Python script on profiler call from Gateway1 start')
    os.system(copy_call_with_args)
    print("remote script invocation form Gateway1 to profiler callend")
    logger.info(f'[{jobid}] : Remote Python script on profiler call from Gateway1 end')


def pushqueue(fileuuid, jobid):

    channel2=connection2.channel()
    channel2.queue_declare("queue_2")

    message = {
        'File_uuid': str(fileuuid),
        'Jobid': jobid
    }
    channel2.basic_publish(exchange='',
                           routing_key='queue_2',
                           body=json.dumps(message))
    print("Message put into receiving (Report) queue")


def on_message_received(ch, method, properties, body):

    json_value=json.loads(body)
    filehash=json_value["File_Hash"]
    jobid=json_value["Job_Id"]
    print(f"received a new filehash= {filehash} and a new jobid = {jobid}")
    logger.info(f'[{jobid}] : received a new file with filehash= {filehash} and Job Id = {jobid}')


    file_path='/home/omr/files/'+filehash+".dat"

    try:
        logger.info(f'[{jobid}] : Calling the copyMalwaretoGW1 function')
        copyMalwareToGW1(filehash, jobid)
    except Exception as e:
        print("error  Occured in the malware copy script")
        logger.info(f'[{jobid}] : Exiting the pullqueue program due to error in the malware copy script - {e}')
        exit(0)

    try:
        logger.info(f'[{jobid}] : Calling the run_remote_python function')
        run_remote_python("192.168.3.1", "jugaad","/home/jugaad/jugaad/Malware/GW1/startTest/omrFiles", "remotestartTestV2.py", filehash, jobid)
    except Exception as e:
        print("error in running script")

    # after the file is received back to the gateway2 after processing by the profiler, it goes to the reports folder and a message is pushed into another queue
    logger.info(f'[{jobid}] : Pushing message of job completion to the Email message queue')
    pushqueue(filehash, jobid)

    print("Job processing complete")
    logger.info(f'[{jobid}] : Job processing completed successfully')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel=connection.channel()

channel.queue_declare("queue_1")


channel.basic_consume(queue='queue_1', auto_ack=False, on_message_callback=on_message_received)
logging.info('Starting the Pulling of messages to Gateway 2')
print("Starting the Pulling of messages to Gateway 2")

channel.start_consuming()


