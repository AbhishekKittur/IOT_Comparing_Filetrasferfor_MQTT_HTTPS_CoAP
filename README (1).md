# README for executing CoAP protocol to transfer the files - 100B, 10KB, 1MB and 10MB from Server to Client.

## File tree structure
- All the files to be transferred from the server should be stored in the same directory as the Server program.
- The Client program will receive all the files and store it in the same directory the client program is stored in.

## Procedure to start Server program
- First, start the server program that is stored on the server by running the command: ``python3 server_CoAP.py``
- The server outputs to standard output, indicating the program has begun : 
```Text
CoAP Server started
``` 

- Once the server program has been started, the client program can be executed and the files can be requested

## Procedure to start Client program
- Start the client program that is stored on the client by running the command: ``python3 client_block_CoAP.py``
- The program will provide the follwoing options via the standard output:
```Text
Choose option:
1. 100B | 2. 10KB | 3. 1MB | 4. 10MB | 5. exit
```
- Number of times each specific file needs to be requested is built into the program, hence only the name of the file needs to be selected by entering the integer option.
- Once a specific file has been received the predetermined number of times, it will provide an output as follows:
```Text
File: xxxx recieved xxxx times
Avg throughput: xxxx.xxxkilobits/s
Standard deviation of throughput: xxx.xxx
Avg application data size divided by file size: x.xxx
```
- To request a different file, the client program needs to be executed again.
