from pymongo import MongoClient
from sanic import Sanic, response

app = Sanic(__name__)
client = MongoClient()
db = client["books"]
collection = db["books"]

# GET /books
@app.route("/books")
async def get_books(request):
    books = list(collection.find({}))
    return response.json(books)

# GET /book/id
@app.route("/book/<book_id>")
async def get_book(request, book_id):
    book = collection.find_one({"id": book_id})
    if book:
        return response.json(book)
    else:
        return response.json({"message": "没找到书籍"}, status=404)

# POST /book/create
@app.route("/book/create", methods=["POST"])
async def create_book(request):
    book_data = request.json
    book = {
        "id": book_data["id"],
        "title": book_data["title"],
        "author": book_data["author"]
    }
    collection.insert_one(book)
    return response.json({"message": "书籍创建成功"})

# PUT /book/update
@app.route("/book/update", methods=["PUT"])
async def update_book(request):
    book_data = request.json
    book_id = book_data["id"]
    update = {"$set": {"title": book_data["title"], "author": book_data["author"]}}
    result = collection.update_one({"id": book_id}, update)
    if result.modified_count > 0:
        return response.json({"message": "书籍更新成功"})
    else:
        return response.json({"message": "Book not found"}, status=404)

# DELETE /book/id
@app.route("/book/<book_id>", methods=["DELETE"])
async def delete_book(request, book_id):
    result = collection.delete_one({"id": book_id})
    if result.deleted_count > 0:
        return response.json({"message": "书籍删除成功"})
    else:
        return response.json({"message": "没找到书籍"}, status=404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)