from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb+srv://pdevaraj:pdevaraj*01@cluster0.qi00g.mongodb.net/inventory?retryWrites=true&w=majority")
mongo = PyMongo(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/inventory', methods=['GET'])
def get_inventory():
    inventory = mongo.db.products.find()
    return jsonify([{"ProductID": item.get("ProductID"), "StockLevel": item.get("StockLevel")} for item in inventory])

@app.route('/inventory', methods=['POST'])
def update_inventory():
    data = request.json
    mongo.db.products.update_one(
        {"ProductID": data.get("ProductID")},
        {"$set": {"StockLevel": data.get("StockLevel"), "LastUpdated": data.get("LastUpdated")}},
        upsert=True
    )
    socketio.emit('update', {"ProductID": data.get("ProductID"), "StockLevel": data.get("StockLevel")})
    return jsonify({"message": "Inventory updated successfully"}), 200

if __name__ == '__main__':
    socketio.run(app, debug=True)
