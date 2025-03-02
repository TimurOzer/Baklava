import socket
import json
import os
import time
import sys
import argparse
from datetime import datetime

class BlockchainClient:
    def __init__(self, server_host='127.0.0.1', server_port=5001, log_folder="client_logs"):
        """
        Initialize the blockchain client
        
        Args:
            server_host: Blockchain server IP address
            server_port: Blockchain server port
            log_folder: Folder to store logs
        """
        self.server_host = server_host
        self.server_port = server_port
        self.log_folder = log_folder
        
        # Create log folder if it doesn't exist
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
            print(f"Log folder created at: {self.log_folder}")
        else:
            print(f"Using existing log folder at: {self.log_folder}")
            
        # Try to import git module, but make it optional
        self.git_available = False
        try:
            import git
            self.git = git
            self.git_available = True
            print("Git integration available")
        except ImportError:
            print("GitPython not installed. Git integration disabled.")
            print("To enable Git integration, install with: pip install GitPython")
    
    def log_message(self, message):
        """
        Log a message to a file with timestamp
        
        Args:
            message: The message to log
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = os.path.join(self.log_folder, f"log_{timestamp}.txt")
        
        with open(log_filename, 'w') as f:
            f.write(message)
            
        print(f"Log saved to: {log_filename}")
        
        # Push to GitHub if available
        if self.git_available:
            try:
                repo = self.git.Repo(search_parent_directories=True)
                repo.git.add(log_filename)
                repo.index.commit(f"New log added: {timestamp}")
                origin = repo.remotes.origin
                origin.push()
                print("Log pushed to GitHub successfully.")
            except Exception as e:
                print(f"GitHub push error: {e}")
    
    def create_transaction(self, sender, recipient, amount):
        """
        Create a new transaction
        
        Args:
            sender: Sender's address
            recipient: Recipient's address
            amount: Transaction amount
        
        Returns:
            Dictionary containing transaction data
        """
        return {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": time.time()
        }
    
    def send_block_to_network(self, block_data=None, password=None):
        """
        Send a block to the blockchain network
        
        Args:
            block_data: Custom block data (optional)
            password: Server authentication password (optional)
        """
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
                # Use provided block data or create a new one
                if block_data is None:
                    # Get transaction details from user
                    sender = input("Enter sender address: ")
                    recipient = input("Enter recipient address: ")
                    amount = input("Enter amount: ")
                    
                    # Create transaction
                    transaction = self.create_transaction(sender, recipient, float(amount))
                    
                    # Create block data
                    block_data = {
                        "index": 1,  # This would normally be determined by the blockchain
                        "previous_hash": "0000",  # This would normally be the hash of the last block
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
        finally:
            client_socket.close()

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Blockchain Client")
    parser.add_argument("--host", default="127.0.0.1", help="Server host address")
    parser.add_argument("--port", type=int, default=5001, help="Server port")
    parser.add_argument("--logs", default="client_logs", help="Log folder path")
    parser.add_argument("--password", help="Server password (optional)")
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()
    
    # Create and run client
    client = BlockchainClient(
        server_host=args.host,
        server_port=args.port,
        log_folder=args.logs
    )
    
    # Send block to network
    client.send_block_to_network(password=args.password)