from sanic import Sanic
from sanic.response import json
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

# 连接数据库
#client = AsyncIOMotorClient('mongodb://localhost:27017')
#db = client['books']
#collection = db['books']

client = MongoClient()
db = client["books"]
collection = db["books"]

# 定义sanic应用
app = Sanic(__name__)

# 封装数据库的crud操作
async def get_books():
    return await collection.find().to_list(None)

async def get_book(id):
    return await collection.find_one({'id': id})

async def create_book(book):
    return await collection.insert_one(book)

async def update_book(id, book):
    return await collection.update_one({'id': id}, {'$set': book})

async def delete_book(id):
    return await collection.delete_one({'id': id})

# 路由
@app.route('/books', methods=['GET'])
async def get_all_books(request):
    books = await get_books()
    return json(books)

@app.route('/book/<id>', methods=['GET'])
async def get_one_book(request, id):
    book = await get_book(id)
    if book:
        return json(book)
    else:
        return json({'message': 'Book not found'}, status=404)

@app.route('/book/create', methods=['POST'])
async def create_one_book(request):
    book = request.json
    if 'id' in book and 'title' in book and 'author' in book:
        await create_book(book)
        return json({'message': 'Book created successfully'}, status=201)
    else:
        return json({'message': 'Book cannot be created'}, status=400)

@app.route('/book/update/<id>', methods=['PUT'])
async def update_one_book(request, id):
    book = request.json
    if 'title' in book or 'author' in book:
        await update_book(id, book)
        return json({'message': 'Book updated successfully'})
    else:
        return json({'message': 'Book cannot be updated'}, status=400)

@app.route('/book/delete/<id>', methods=['DELETE'])
async def delete_one_book(request, id):
    book = await get_book(id)
    if book:
        await delete_book(id)
        return json({'message': 'Book deleted successfully'})
    else:
        return json({'message': 'Book does not exist'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)