import socket
import json
import os
import time
import sys
import traceback
from datetime import datetime

# Error logging function
def log_error(error_msg, traceback_info=None):
    """Log errors to a file to help with debugging the executable"""
    error_log_path = "client_error.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(error_log_path, "a") as f:
        f.write(f"[{timestamp}] ERROR: {error_msg}\n")
        if traceback_info:
            f.write(f"Traceback:\n{traceback_info}\n")
        f.write("-" * 50 + "\n")
    
    print(f"Error logged to: {error_log_path}")

class BlockchainClient:
    def __init__(self, server_host='127.0.0.1', server_port=5001, log_folder="client_logs"):
        """Initialize the blockchain client"""
        self.server_host = server_host
        self.server_port = server_port
        self.log_folder = log_folder
        
        try:
            # Create log folder if it doesn't exist
            if not os.path.exists(self.log_folder):
                os.makedirs(self.log_folder)
                print(f"Log folder created at: {self.log_folder}")
            else:
                print(f"Using existing log folder at: {self.log_folder}")
        except Exception as e:
            print(f"Warning: Could not create log folder: {str(e)}")
            # Set folder to current directory as fallback
            self.log_folder = "."
    
    def log_message(self, message):
        """Log a message to a file with timestamp"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_filename = os.path.join(self.log_folder, f"log_{timestamp}.txt")
            
            with open(log_filename, 'w') as f:
                f.write(message)
                
            print(f"Log saved to: {log_filename}")
        except Exception as e:
            print(f"Warning: Could not save log: {str(e)}")
    
    def create_transaction(self, sender, recipient, amount):
        """Create a new transaction"""
        return {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": time.time()
        }
    
    def send_block_to_network(self, password=None):
        """Send a block to the blockchain network"""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Connect to server
            print(f"Connecting to server at {self.server_host}:{self.server_port}...")
            client_socket.connect((self.server_host, self.server_port))
            print("Connected to server.")
            
            # Get password if not provided
            if password is None:
                password = input("Please enter the server password: ")
                
            # Send password
            client_socket.send(password.encode('utf-8'))
            
            # Get server response
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")
            
            if response == "Password accepted":
                # Get transaction details from user
                sender = input("Enter sender address: ")
                recipient = input("Enter recipient address: ")
                amount = input("Enter amount: ")
                
                # Create transaction
                transaction = self.create_transaction(sender, recipient, float(amount))
                
                # Create block data
                block_data = {
                    "index": 1,
                    "previous_hash": "0000",
                    "transactions": transaction,
                    "timestamp": time.time()
                }
            
                # Send block data
                client_socket.send(json.dumps(block_data).encode('utf-8'))
                print(f"Sent block data: {json.dumps(block_data, indent=2)}")
                
                # Get server response
                response = client_socket.recv(1024).decode('utf-8')
                print(f"Server response: {response}")
                
                # Log the transaction
                log_message = (
                    f"Transaction sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Block data: {json.dumps(block_data, indent=2)}\n"
                    f"Server response: {response}\n"
                )
                self.log_message(log_message)
            else:
                print("Authentication failed. Cannot send block data.")
                
        except ConnectionRefusedError:
            print(f"Error: Could not connect to server at {self.server_host}:{self.server_port}")
            print("Make sure the server is running and the address is correct.")
        except Exception as e:
            print(f"Error: {e}")
            # Log the error
            log_error(str(e), traceback.format_exc())
        finally:
            client_socket.close()

def main():
    """Main entry point for the application"""
    try:
        # Display startup message
        print("Blockchain Client Starting...")
        print(f"Working Directory: {os.getcwd()}")
        
        # Ask for server details
        server_host = input("Enter server IP (or press Enter for default 127.0.0.1): ")
        if not server_host:
            server_host = "127.0.0.1"
            
        server_port_str = input("Enter server port (or press Enter for default 5001): ")
        server_port = int(server_port_str) if server_port_str else 5001
        
        # Create and run client
        client = BlockchainClient(
            server_host=server_host,
            server_port=server_port
        )
        
        # Send block to network
        client.send_block_to_network()
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        error_message = f"Unhandled exception: {str(e)}"
        print(error_message)
        print(error_traceback)
        log_error(error_message, error_traceback)
    
    # Keep console open
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()