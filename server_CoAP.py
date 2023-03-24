import asyncio
import aiocoap.resource as resource
import aiocoap

class fileReturn(resource.Resource):
    """
    Defining a server resource
    """
    async def render_get(self, request):
        """
        Resource function for handing GET requests 

        Argument:
	    request -- Request received from client that is to be processed by the server 

	    Returns:
	    aiocoap Message with required payload to be sent to client
        """
        #Reading payload of client to retrieve the file client requested using request payload
        file_name = request.payload.decode("utf-8") 

        #Opening and reading the specified file. 
        #Ensure all 4 files must be in same directory as server file, else change path to read file
        data = open(str(file_name), 'rb')
        byte_data = data.read()

        #Creating response message with the requested file's content
        return aiocoap.Message(payload=byte_data)


async def main():
    #Creating server resources
    root = resource.Site()

    #Mapping resource path with server object to handle requests regarding specific resources
    #In this case reading specific files and returning the data
    root.add_resource(['file'], fileReturn())

    #Create a server context to bind to a port, along with establishing start of resources of server
    await aiocoap.Context.create_server_context(bind=('127.0.0.1',5683),site=root)
    #await aiocoap.Context.create_server_context(root)

    #Continue running the server to process all requests until a terminate signal(such as keyboard interrupt)
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    print("CoAP Server started")
    asyncio.run(main())
