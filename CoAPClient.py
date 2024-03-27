from coapthon.client.helperclient import HelperClient

# CoAP server endpoint URL
server_host = "192.168.137.230"  # Replace with your Arduino's IP address
server_port = 5683  # Default CoAP port

# Initialize the CoAP client
client = HelperClient(server=(server_host, server_port))

while True:
    user_input = input("Enter 'on' to turn the LED on, 'off' to turn it off, or 'exit' to quit: ")
    
    if user_input == 'exit':
        break
    elif user_input == 'on':
        payload = "1"
    elif user_input == 'off':
        payload = "0"
    else:
        print("Invalid input. Please enter 'on', 'off', or 'exit'.")
        continue
    
    # Send CoAP PUT request based on user input
    response = client.put("light", payload)
    print("Response Code:", response.code)

# Close the client connection
client.stop()
