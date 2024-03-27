import asyncio
from aiocoap import *

async def coap_put(host, path, payload):
    protocol = await Context.create_client_context()
    request = Message(code=PUT, uri=f"coap://{host}/{path}", payload=payload.encode('utf-8'))
    try:
        response = await protocol.request(request).response
        print(f"Response Code: {response.code}")
    except Exception as e:
        print(f"Failed to send CoAP request: {e}")

async def main():
    host = "192.168.137.84"  # Replace with your Arduino's IP address
    path = "light"  # Endpoint for controlling the LED on Arduino
    #while True:
    try:
        user_input = input("Enter 'on' to turn the LED on, 'off' to turn it off, or 'exit' to quit: ")
##        if user_input == 'exit':
##            break
        if user_input in ('on', 'off'):
            payload = '1' if user_input == 'on' else '0'
            await coap_put(host, path, payload)
        else:
            print("Invalid input. Please enter 'on', 'off', or 'exit'.")
    except asyncio.CancelledError:
        print("Task cancelled.")

if __name__ == "__main__":
    asyncio.run(main())
