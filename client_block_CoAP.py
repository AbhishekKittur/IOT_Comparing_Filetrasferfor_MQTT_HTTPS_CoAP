import asyncio
from aiocoap import *
from aiocoap import optiontypes, message
import timeit
import statistics
import logging
logging.getLogger().setLevel(logging.CRITICAL)


def avg_std(data, stat):
	"""
	avg_std calculates the average of a list or the standard deviation of the list
	
	Argument:
	data -- List, Python list with numerical values
	stat -- String, 'avg' to calculate list average, 'std_dev' to calculate standard deviation of list values

	Returns:
	Average or Standard Deviation
	"""
	if stat == "avg" : return round(sum(data)/len(data), 3)
	if stat == "std_dev" : return round(statistics.stdev(data), 3)


async def send_request_man_block(uri, file):
	"""
	send_request_man_block requests a file from the server and handles large data(bigger than coap block size)
	in a blockwise manner until all blocks are received and appended to the file
	
	Argument:
	uri -- url of server and the path for the server resource
	file -- file name to be requested from the server

	Returns:
	total_req_time -- Total time taken to recieve response for the request
	complete_resp_size -- Total response size, including header and payload data
	"""
	#Create a client context on a random listening port. This is the easiest way to get a context suitable for sending client requests.
	protocol = await Context.create_client_context()

	#CoAP Message with some handling metadata, This object’s attributes provide access to the fields in a CoAP message
	#Method is set to GET, payload contains file name to request, message type is confirmable message with uri passed to function
	request = Message(code=GET, payload=file.encode('utf-8'), mtype=CON, uri=uri)

	#Start time of request
	req_start_time = timeit.default_timer()

	#Request message object sent to server with blockwise handling of response set to False
	response = await protocol.request(request, handle_blockwise=False).response

	#Complete reponse received, contains payload and CoAP header data
	complete_resp_size = len(response.encode())

	#Create new file to write all data, if file exists open it in read+write mode to write data of each block to the open file
	try:
		#time.sleep(10)
		f = open(file, 'xb')
	except:
		f = open(file, 'wb')
	
	#Write all data in first block
	f.write(response.payload)

	#Iterate until response options block2 more = False, meaning all blocks received
	while True:
		#If additional block data is present after current block, request for next block
		if response.opt.block2 and response.opt.block2.more:
			
			#Increment block number, use previous exponenet number in new request
			request.opt.block2 = optiontypes.BlockOption.BlockwiseTuple(response.opt.block2.block_number+1, 0, response.opt.block2.size_exponent)
			response = await protocol.request(request, handle_blockwise=False).response

			#Add received response size to response size variable and append to open file the new data
			complete_resp_size += len(response.encode())
			f.write(response.payload)
		else:
			#If no more blocks left, exit loop
			break

	#All data recieved, measure request end time
	req_end_time = timeit.default_timer()

	f.close()
	
	#Calculate total request time by subtracting end time and start time
	total_req_time = req_end_time-req_start_time
	return total_req_time, complete_resp_size


async def send_request_auto_block(uri, file):
	"""
	send_request_auto_block requests a file from the server and handles large data(bigger than coap block size)
	automatically using aiocoap's blockwise option
	
	Argument:
	uri -- url of server and the path for the server resource
	file -- file name to be requested from the server

	Returns:
	total_req_time -- Total time taken to recieve response for the request
	complete_resp_size -- Total response size, including header and payload data
	"""
	protocol = await Context.create_client_context()
	req_start_time = time.time()
	request = Message(code=GET, payload=file.encode('utf-8'), mtype=CON, uri=uri)
	response = await protocol.request(request, handle_blockwise=True).response
	complete_resp_size = len(response.encode())
	try:
			f = open(file, 'xb')
	except:
			f = open(file, 'wb')
	f.write(response.payload)
	f.close()
	req_end_time = time.time()
	total_req_time = req_end_time-req_start_time
	return total_req_time, complete_resp_size


async def main():
	print("Choose option:")	
	option = int(input("1. 100B | 2. 10KB | 3. 1MB | 4. 10MB | 5. exit\n"))
	if option > 4 : return 0

	#Dictionary with file name and number of times it needs to be requested
	files_dict = {
		1:["100B", 10000],
		2:["10KB", 1000],
		3:["1MB", 100],
		4:["10MB", 10],
	}

	#Extract file name and number of times to get the file 
	file_req_name = files_dict[option][0]
	num_iter = files_dict[option][1]

	#Lists to record time, throughput and appn. layer data for each iteration of the file requests
	time_records = []
	throughputs = []
	application_data = []

	#Define uri. Contains protocol, ip address and resource path in server
	uri = "coap://127.0.0.1/file"
	#uri = "coap://192.168.1.132/file"

	print(f"\nRequesting file: {file_req_name}, {num_iter} times")

	#Iterate over the required number of times file needs to be received
	for i in range(num_iter):
		one_req_time, total_response_size = await send_request_man_block(uri, file_req_name)
		#one_req_time, total_response_size = await send_request_auto_block(uri, file_req_name)

		#Open the file in binary mode saved by send_request_man_block() to get the content size(used for throughput calculation)
		data = open(file_req_name, 'rb')
		data_size = data.read()

		#Calculate throughput. Multiple file content size by 8 to convert bytes to bits. Divide by time taken to recieve file and by 1024 to convert to kilobits
		tp = (len(data_size)*8)/((one_req_time)*1024)
		
		#Calculate ration of total application layer response to file size
		#Add all values to corresponding lists
		application_data.append(total_response_size/len(data_size))
		time_records.append(one_req_time)
		throughputs.append(tp)

		print(f"Done with {i+1} file request, took {one_req_time}s")


	#Print all metrics and values
	print(f"\nFile: {file_req_name} recieved {num_iter} times")
	#print(f"Times are: {time_records}")
	#print(f"Avg time taken: {avg_std(time_records, 'avg')}s")
	#print(f"Standard deviation of time: {avg_std(time_records, 'std_dev')}")
	#print(f"Throughputs are: {throughputs}")
	print(f"Avg throughput: {avg_std(throughputs, 'avg')}kilobits/s")
	print(f"Standard deviation of throughput: {avg_std(throughputs, 'std_dev')}")
	#print(f"Application data sizes divided by file size: {app_data}")
	print(f"Avg application data size divided by file size: {avg_std(application_data, 'avg')}")


if __name__ == "__main__":
	asyncio.run(main())