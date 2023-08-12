from sanic import Sanic
from sanic.response import json
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import json as json_module
from pymongo import MongoClient

app = Sanic(__name__)
#连数据库
mongodb_uri = "mongodb://localhost:27017"
database_name = 'usermanage'

#client = MongoClient()
#db = client["usermanage"]

class db:
    def __init__(self, db_url):
        self.client = MongoClient(db_url)
        self.db = self.client['usermanage']
        self.users_collection = self.db['users']
        self.limit_collection = self.db['limit']
        self.department_collection = self.db['department']

    async def get_users(self):
        return await self.users_collection.find().to_list(None)

    async def get_user(self, id):
        return await self.users_collection.find_one({'id': id})

    async def create_user(self, user):
        return await self.users_collection.insert_one(user)

    async def update_user(self, id, user):
        result = await self.users_collection.update_one({'id': id}, {'$set': user})

    async def delete_user(self, id):
        return await self.users_collection.delete_one({'id': id})

    async def get_limit(self, limitname,user):
        return await self.limit_collection.find_one({'limitname': limitname,'user':user})

    async def create_limit(self, limit):
        return await self.limit_collection.insert_one(limit)

    async def update_limit(self, limitname, user, limit):
        return await self.limit_collection.update_one({'limitname': limitname, 'user': user}, {'$set': limit})

    async def delete_limit(self, limitname, user):
        return await self.limit_collection.delete_one({'limitname': limitname, 'user': user})

    async def get_department(self, department):
        return await self.department_collection.find_one({'department': department})

    async def create_department(self, department):
        return await self.department_collection.insert_one(department)

    async def update_department(self, department, newdepartment):
        return await self.department_collection.update_one({'department': department}, {'$set': newdepartment})

    async def delete_department(self, department):
        return await self.department_collection.delete_one({'department': department})

@app.route('/users', methods=['GET'])
async def get_all_users(request):
    users = await db.get_users()
    return json(users)

@app.route('/user/<id>', methods=['GET'])
async def get_one_user(request, id):
    user = await db.get_user(id)
    if user:
        return json(user)
    else:
        return json({'message': 'user not found'}, status=404)

@app.route('/user/create', methods=['POST'])
async def create_one_user(request):
    user = request.json
    if 'id' in user and 'name' in user and 'department' in user and 'position' in user and 'number' in user and 'emile' in user and 'time' in user and 'limit' in user:
        await db.create_user(user)
        return json({'message': 'user created successfully'}, status=201)
    else:
        return json({'message': 'user cannot be created'}, status=400)

@app.route('/user/update/<id>', methods=['PUT'])
async def update_one_user(request, id):
    user_data = request.json
    user = await db.get_user(id)
    if user:
        await db.update_user(id, user_data)
        return json({'message': 'user updated successfully'})
    else:
        return json({'message': 'user cannot be updated'}, status=400)

@app.route('/user/delete/<id>', methods=['DELETE'])
async def delete_one_user(request, id):
    await db.delete_book(id)
    return json({'message': 'user deleted successfully'})

@app.route('/limit/create', methods=['POST'])
async def create_one_limit(request):
    limit = request.json
    if 'limitname' in limit and 'user' in limit :
        await db.create_user(limit)
        return json({'message': 'limit created successfully'}, status=201)
    else:
        return json({'message': 'limit cannot be created'}, status=400)

@app.route('/limit/update/<id>', methods=['PUT'])
async def update_one_limit(request, limitname,user):
    limit_data = request.json
    limit = await db.get_limit(limitname,user)
    if limit:
        await db.update_limit(limitname,user, limit_data)
        return json({'message': 'limit updated successfully'})
    else:
        return json({'message': 'limit cannot be updated'}, status=400)

@app.route('/limit/delete/<id>', methods=['DELETE'])
async def delete_one_limit(request, limitname,user):
    await db.delete_book(limitname,user)
    return json({'message': 'limit deleted successfully'})

@app.route('/department/create', methods=['POST'])
async def create_one_department(request):
    department = request.json
    if 'department' in department :
        await db.create_department(department)
        return json({'message': 'department created successfully'}, status=201)
    else:
        return json({'message': 'department cannot be created'}, status=400)

@app.route('/department/update/<id>', methods=['PUT'])
async def update_one_limit(request, department):
    department_data = request.json
    department = await db.get_limit(department)
    if department:
        await db.update_limit(department, department_data)
        return json({'message': 'department updated successfully'})
    else:
        return json({'message': 'department cannot be updated'}, status=400)

@app.route('/department/delete/<id>', methods=['DELETE'])
async def delete_one_department(request, department):
    await db.delete_book(department)
    return json({'message': 'department deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)