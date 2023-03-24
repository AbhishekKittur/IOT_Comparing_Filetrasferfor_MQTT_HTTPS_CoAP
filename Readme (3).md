# File transfer using MQTT - QoS2

The objective of this project is to accomplish a successful file transfer between the publisher and subscriber via the MQTT broker.
For each experiment, we aim to transfer 100 bytes, 1MB, 10KB, and 10MB files. A series of experiments must be carried out in order to study the average throughput trend when transferring various files using MQTT QoS2.

For this publisher and subscriber implementation, we use the Paho MQTT Client Python library. The Eclipse mosquitto broker is used as the MQTT broker. This broker is downloaded and installed locally, and it runs a broker to enable this file transfer.

To conduct our experiments , we run the publisher , the subscriber and the broker in the same PC using the loopback address - 127.0.0.1 for the broker. The publisher and the subscriber establish the connection with this broker. 

NOTE: We attempted to run the publisher, subscriber, and broker on separate PCs connected to the same LAN, but the Mosquitto broker actively refused any client connection to its socket. Even after disabling all firewalls on the PC and changing the mosquitto.conf file to listen at the public IP address of the PC where the broker is running, the problem persisted.

# Libraries used

a) paho.mqtt.client -> For implementing the MQTT Publisher and subscriber
b) time -> For calculating the time taken for the file transfer
c) sys -> To find the payload size (application layer data + header)
d) Eclipse mosquitto -> To run the broker service locally in a PC
e)Statistics -> To find the Standard Deviation values after calculating the Throughput

# Implementation

This Project has - 
1) Four data files (100 bytes, 1MB, 10KB and 10MB files)
2) Publisher - publisher.py
3) Subscriber - subscriber.py


1) Install the mosquitto broker service for windows from - https://mosquitto.org/download/

2) After a successful installation, launch the command prompt as administrator and change the current directory to the folder containing the Mosquitto configuration files.

An example would be -
`cd C:\ProgramFiles\mosquitto`

3) The mosquitto broker is then started in verbose mode at the loopback address - 127.0.0.1. (mosquitto broker service will by default run at that IP, port 1883)

`mosquitto -v`

4) Then we start the subscriber running at the Loopback address - 127.0.0.1 by running the following command in Terminal - 1 :

`python3 subscriber_QoS2.py`

From the broker logs - you can observe a successful connection from the client (subscriber). You will be prompted to choose the file you want to receive. Choose the option.

5) Next we run Publisher (running at the Loopback address - 127.0.01). Run the following command in Terminal - 2:

`python3 publisher_QoS2.py`

From the broker logs - you can observe a successful connection from the publisher. You will be prompted to choose the file you want to send. Choose the option. Note that the file you wish to send from the publisher should be same as the file you wish to receive on the subscriber end.

6) Observe the broker logs to check for the message transfer while the file is sent from the publisher to broker and then from the broker to subscriber. On the subscriber end, received_file.txt will be created indicating successful file transfer. The average throughput, standard deviation, total application layer data / file size will be displayed in the stdout respectively.

# Implicit definitions / assumptions

- The time taken for file transfer in this implementation is defined as the time taken for the file to transfer from the publisher to the broker successfully.
- Each file (100 bytes, 1MB, 10KB or 10MB) is published to a different file topic and subscribed accordingly.
- On the subscriber end, we create a received_file.txt each time we receive a file (for num_iters) and keep rewriting this file.
- In order to find the total payload size containing the application layer data and the header , we find the size of the message.payload where message is a MQTT Message object.