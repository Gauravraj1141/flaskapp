from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
mongo = PyMongo(app)

# GET /users - Returns a list of all users.
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    result = []
    for user in users:
        result.append({
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email']
        })
    return jsonify(result)

# GET /users/<id> - Returns the user with the specified ID.
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    try:
        user = mongo.db.users.find_one({'_id': ObjectId(id)})
        result = {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email']
        }
    except Exception as ex:
        result = {"status":404,"message":ex}
    return jsonify(result)

# POST /users - Creates a new user with the specified data.
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = {
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
    }
    result = mongo.db.users.insert_one(user)
    return jsonify({'id': str(result.inserted_id)}), 201

# PUT /users/<id> - Updates the user with the specified ID with the new data.
@app.route('/users/<string:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = mongo.db.users.find_one_or_404({'_id': ObjectId(id)})
    user['name'] = data['name']
    user['email'] = data['email']
    user['password'] = data['password']
    mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': user})
    return jsonify({'message': 'User updated successfully'})

# DELETE /users/<id> - Deletes the user with the specified ID.
@app.route('/users/<string:id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
