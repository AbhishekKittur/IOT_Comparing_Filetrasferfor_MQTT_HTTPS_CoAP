# README for executing Http protocol to transfer the files - 100B, 10KB, 1MB and 10MB from Server to Client.

## File tree structure
- All the files to be transferred from the server should be stored in the same directory as the Server program.
- The Client program will receive all the files and store it in the same directory the client program is stored in.

## Procedure to start Server program
- First, start the server program that is stored on the server by running the command: ``python3 HttpServer.py``
- The server outputs to standard output, indicating the program has begun : 
```Text
http server is starting...
http server is running...
``` 
The http server prints HTTP Response msg for each file transfer

- Once the server program has been started, the client program can be executed and the files can be requested

## Procedure to start Client program
- Start the client program that is stored on the client by running the command: ``python3 HttpClient.py``
- The program will run and request files one by one from server. 
- Number of times each specific file needs to be requested is built into the program, the name of the file is used to request the file from server .
- Once a specific file has been received the predetermined number of times, it will provide an output as follows:
```Text
Downloading File: xxxx 
##### Sending Request to Server for: {file_xxx} --{yyy} times #####
Average throughput in kilobits per second: xxxx.xxx
Throughput Standard Deviation in kilobits per second: xxx.xxx
Average Application Layer data received per file size: x.xxx
##### File download complete for: {file_xxx} #####
```
The program runs for all files and displays results for all the files one by one.  
