
# from Database.userDB import db
# from flask import request,jsonify,Blueprint

# userApp = Blueprint('user',__name__)


# @userApp.route('/users',methods=['POST'])
# def createUser():
#     data = request.json
#     name = data.get('name')
#     password = data.get('password')
#     email = data.get('email')

#     if not name or not password or not email:
#         return jsonify({"error": "Missing required fields"}), 400
    
#     newUserID = db.addUser(data['name'],data['email'],data['password'])


#     if isinstance(newUserID, str):
#         # User was successfully created
#         return jsonify({"message": "User created successfully", "user_id": newUserID}), 201
#     else:
#         # User already exists
#         return jsonify({"error": "User with this email or name already exists"}), 400

# @userApp.route('/users',methods=['GET'])
# def getUsers():
#     users = db.allUsers()
#     for user in users:
#         user['_id'] = str(user['_id'])
#         del user['password'] 
#     return jsonify(users)


# @userApp.route('/users/<userID>',methods=['GET'])
# def getUser(userID):
#     user = db.findUser(userID)
#     if user:
        
#         user['_id'] = str(user['_id'])
#         user['password'] = str(user['password'])
#         # print(user)
#         return jsonify(user)
#     return jsonify({'Error':'No user found with this ID'}),404

# @userApp.route('/users/<userID>',methods=['PUT'])
# def updateUser(userID):
#     data = request.json
#     if db.updateUser(userID,data):
#         return jsonify({'Success':'User Data Update'})

#     return jsonify({'error': 'User not found'}), 404

# @userApp.route('/users/<userID>', methods=['DELETE'])
# def delete_user(userID):
#     if db.delUser(userID):
#         return jsonify({'message': 'User deleted successfully'})
#     return jsonify({'error': 'User not found'}), 404

from flask_restful import Resource, reqparse
from Database.userDB import db

class UserResource(Resource):
    def get(self, user_id):
        user = db.findUser(user_id)
        if user:
            user['_id'] = str(user['_id'])
            user['password'] = str(user['password'])
            return user
        return {'Error': 'No user found with this ID'}, 404

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        data = parser.parse_args()

        if db.updateUser(user_id, data):
            return {'Success': 'User Data Updated'}
        return {'error': 'User not found'}, 404

    def delete(self, user_id):
        if db.delUser(user_id):
            return {'message': 'User deleted successfully'}
        return {'error': 'User not found'}, 404

class UserListResource(Resource):
    def get(self):
        users = db.allUsers()
        for user in users:
            user['_id'] = str(user['_id'])
            del user['password']
        return users

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
        parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")
        data = parser.parse_args()

        new_user_id = db.addUser(data['name'], data['email'], data['password'])

        if isinstance(new_user_id, str):
            return {"message": "User created successfully", "user_id": new_user_id}, 201
        else:
            return {"error": "User with this email or name already exists"}, 400