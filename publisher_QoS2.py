import paho.mqtt.client as mqtt
#This module provides a client class which enable applications to connect to an MQTT broker to publish messages, and to subscribe to topics and receive published messages.
import time
#The time module provides many ways of representing time in code, such as objects, numbers, and strings.
import sys
#This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
import statistics
#This module provides functions for calculating mathematical statistics of numeric ( Real -valued) data

# Global parameters
broker_ip = "127.0.0.1"
start_time = 0
file_req_name = "filename"
num_iter = 0
time_record = []
throughput_record = []
data_size = 0

def on_connect(client, userdata, flags, rc):
    """
    on_connect is a callback function which is called when the publisher makes a successful TCP connection with the broker

    arguments: 
    client - Class object, The paho mqtt client object - used to perform the client operations like subscribe and publish
    rc - int, Return code indicating the status of the connection between the publisher and broker

    Assigns the topic name which the client has to publish to and the client publishes to the broker accordingly num_iter times.
    We calculate the start_time as the time at which the file is sent from the publisher side.
    
    """
    global start_time
    global data_size
    global throughput_record
    print("Connected with result code "+str(rc)) #Will show Connected with result code 0, means connected successfully
    if file_req_name == "100B":
        topic_name = "file_transfer_100B"
        data_size = 100
    elif file_req_name == "10KB":
        topic_name = "file_transfer_10KB"
        data_size = 10000
    elif file_req_name == "1MB":
        topic_name = "file_transfer_1MB"
        data_size = 1000000
    elif file_req_name == "10MB":
        topic_name = "file_transfer_10MB"
        data_size = 10000000

    for i in range(num_iter):
        file = open(file_req_name, "rb")
        data = file.read()
        file.close()
        start_time = time.time()  
        client.publish(topic_name, data, qos=2)

def on_publish(client, userdata, mid):
    """
    on_publish is a callback function which is called when the publisher successfully publishes the data to the broker and receives an ACK

    arguments: 
    client - Class object, The paho mqtt client object - used to perform the client operations like subscribe and publish
    mid - int, Message ID of the message being published to the broker

    On successfully publishing the file to the broker each iteration, we track the end time and hence calculate the total time taken for this file transfer.
    The total time taken for the file transfer is defined as the duration between the publisher sending the file and the broker successfully receives it 
    on the corresponding topic. Then we calculate the average throughput in kb/s ad the standard deviation of this throughput.
    
    """
    global throughput_record
    print("Message published to broker with message id:", mid)
    end_time = time.time() 
    total_time = end_time - start_time
    time_record.append(total_time)
    calculate_throughput(total_time, throughput_record)
    if len(time_record) == num_iter:
        print(f"Avg throughput: { round(sum(throughput_record)/len(throughput_record), 3)} kilobits/s")
        print(f"Standard deviation of throughput: {round(statistics.stdev(throughput_record))}")

def calculate_throughput(total_time, throughput_record):
    
    """
    To calculate Avg throughput when the file is transferred for num_iter times

    arguments:
    total_time: Int, The time duration between the file being sent from the publisher and the time at which the broker receives it
    throughput_record: List, A list of the throughputs for each file transfer num_iter times
    
    """
    tp = (data_size*8)/((total_time)*1024)
    throughput_record.append(tp)


if __name__ == "__main__":
    print("Choose option:")	
    option = int(input("1. 100B | 2. 10KB | 3. 1MB | 4. 10MB | 5. exit\n")) #File sizes required to be transfered depending upon the the option selection
    if option > 4 : 
        print("Choose a valid option")
        sys.exit()

    files_dict = {                         
		1:["100B", 10000],
		2:["10KB", 1000],
		3:["1MB", 100],
		4:["10MB", 10],
	}

    #Extract file name and number of times to get the file 
    file_req_name = files_dict[option][0]  # Get the file ie 100B, 10KB.. from here
    num_iter = files_dict[option][1]   #Get the number of iterations for the file to run fro here

    client = mqtt.Client("Publisher")
    client.on_connect = on_connect  #call back function to .on_connect
    client.on_publish = on_publish  #call back function to .on_publish
    client.connect(broker_ip, 1883, 60) #Connection to broker on broker IP 127.0.0.1, Port number 1883 and Keep Alive Timer of 60

    client.loop_forever() 
