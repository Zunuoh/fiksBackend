from flask import Flask, jsonify, request, Blueprint

customers = Blueprint('customers', __name__, url_prefix='/customers')


# @customers.route('/customer', methods=['POST'])
# def add_customer():
#     try:

#     except