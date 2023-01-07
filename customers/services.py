import json

class CustomerServices:

    def add_customer(self, request_data):
        try:
            name = request_data.get('name')
            lastName = request_data.get('lastName')
            print("nameeee", name)
            
