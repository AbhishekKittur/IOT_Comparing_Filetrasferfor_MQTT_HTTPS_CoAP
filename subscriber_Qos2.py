import paho.mqtt.client as mqtt  
#This module provides a client class which enable applications to connect to an MQTT broker to publish messages, and to subscribe to topics and receive published messages. 
import sys
#This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter

# Global Parameters
broker_ip = "127.0.0.1"
file_req_name = "filename"
num_iter = 0
appln_data_avg = []
data_size = 0
msg_count = 1


def on_connect(client, userdata, flags, rc):
    """
    on_connect is a callback function which is called when the subscriber makes a successful TCP connection with the broker

    arguments: 
    client - Class object, The paho mqtt client object - used to perform the client operations like subscribe and publish
    rc - int, Return code indicating the status of the connection between the publisher and broker

    The client subscribes to the corresponding topic that the publisher publishes to depending on the user's choice
    """
    global data_size
    print("Connected with result code "+str(rc))
    if file_req_name == "100B":
        client.subscribe("file_transfer_100B", qos=2)
        data_size = 100
    elif file_req_name == "10KB":
        client.subscribe("file_transfer_10KB", qos=2)
        data_size = 10000
    elif file_req_name == "1MB":
        client.subscribe("file_transfer_1MB", qos=2)
        data_size = 1000000
    elif file_req_name == "10MB":
        client.subscribe("file_transfer_10MB", qos=2)
        data_size = 10000000
        


def on_message(client, userdata, message):
    """
    on_message is a callback function which is called when the subscriber receives a message from the broker

    arguments: 
    client - Class object, The paho mqtt client object - used to perform the client operations like subscribe and publish
    message - Class object, Contains the topic, QoS and the payload info 

    The client receives the message and writes it to the received_file.txt each time on the subscriber side. In order to calculate the 
    total application layer data/ file size , we calculate the total application layer data as application layer data + the header content (size of the msg.payload).
    """
    global appln_data_avg
    global msg_count
    payload_size = sys.getsizeof(message.payload)

    file = open("received_file.txt", "wb")
    file.write(message.payload)
    file.close()

    application_data = payload_size / data_size
    appln_data_avg.append(application_data)
    msg_count += 1

    if msg_count == num_iter:
        print("Avg application data sizes divided by file size:", round(sum(appln_data_avg)/len(appln_data_avg), 3))


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
    num_iter = files_dict[option][1]  #Get the number of iterations for the file to run fro here

    client = mqtt.Client("Subscriber")
    client.on_connect = on_connect #call back function to .on_connect
    client.on_message = on_message #call back function to .on_publish

    client.connect(broker_ip, 1883, 60) #Connection to broker on broker IP 127.0.0.1, Port number 1883 and Keep Alive Timer of 60

    client.loop_forever()
    
