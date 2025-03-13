# 🎵 Song Management API

Welcome to the **Song Management API**! 🎶 This RESTful API provides endpoints for managing a collection of songs. It supports basic CRUD (Create, Read, Update, Delete) operations for song resources. Below you'll find the details of the available endpoints, solutions, and some additional guidelines for the API.

 ![Back End Development Songs](https://github.com/Willie-Conway/Back-End-Development-Songs/blob/c7902455ce6a2988ed974963d9254e51273afc70/Screenshots/Back%20End%20Development%20Songs.gif)

---

## 🎯 Objectives

- **Start MongoDB database server** 🗄️
- **Create a Flask server** ⚡
- **Write RESTful APIs** for managing song resources 🎶
- **Test the APIs** 🧪

---

## 🚀 RESTful API Endpoints

| Action | Method | Return Code | Body | URL Endpoint |
|--------|--------|-------------|------|--------------|
| **List** | GET | 200 OK | Array of songs `[{...}]` | `/song` |
| **Create** | POST | 201 CREATED | A song resource as JSON `{...}` | `/song` |
| **Read** | GET | 200 OK | A song as JSON `{...}` | `/song/{id}` |
| **Update** | PUT | 200 OK | A song as JSON `{...}` | `/song/{id}` |
| **Delete** | DELETE | 204 NO CONTENT | "" | `/song/{id}` |
| **Health** | GET | 200 OK | "" | `/health` |
| **Count** | GET | 200 OK | "" | `/count` |

---

## 💡 Solutions

This page contains the solutions for the List, Create, Update, and Delete REST APIs.

### 🩺 Health
Check if the API is healthy and running.
```python
@app.route("/health")
def healthz():
    return jsonify(dict(status="OK")), 200
```

### 📊 Count
Get the number of songs in the database.
```python
@app.route("/count")
def count():
    """return length of data"""
    count = db.songs.count_documents({})
    return {"count": count}, 200
```

### 🎤 List
Retrieve all the songs from the database.
```python
@app.route("/song", methods=["GET"])
def songs():
    # docker run -d --name mongodb-test -e MONGO_INITDB_ROOT_USERNAME=user
    # -e MONGO_INITDB_ROOT_PASSWORD=password -e MONGO_INITDB_DATABASE=collection mongo
    results = list(db.songs.find({}))
    print(results[0])
    return {"songs": parse_json(results)}, 200
```

### 🎧 Read
Get a specific song by its ID.
```python
@app.route("/song/<int:id>", methods=["GET"])
def get_song_by_id(id):
    song = db.songs.find_one({"id": id})
    if not song:
        return {"message": f"song with id {id} not found"}, 404
    return parse_json(song), 200
```

### ✍️ Create
Create a new song in the database.
```python
@app.route("/song", methods=["POST"])
def create_song():
    # get data from the json body
    song_in = request.json
    print(song_in["id"])
    # if the id is already there, return 303 with the URL for the resource
    song = db.songs.find_one({"id": song_in["id"]})
    if song:
        return {
            "Message": f"song with id {song_in['id']} already present"
        }, 302
    insert_id: InsertOneResult = db.songs.insert_one(song_in)
    return {"inserted id": parse_json(insert_id.inserted_id)}, 201
```

### 🛠️ Update
Update an existing song by its ID.
```python
@app.route("/song/<int:id>", methods=["PUT"])
def update_song(id):
    # get data from the json body
    song_in = request.json
    song = db.songs.find_one({"id": id})
    if song == None:
        return {"message": "song not found"}, 404
    updated_data = {"$set": song_in}
    result = db.songs.update_one({"id": id}, updated_data)
    if result.modified_count == 0:
        return {"message": "song found, but nothing updated"}, 200
    else:
        return parse_json(db.songs.find_one({"id": id})), 201
```

### 🗑️ Delete
Delete a song by its ID.
```python
@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):
    result = db.songs.delete_one({"id": id})
    if result.deleted_count == 0:
        return {"message": "song not found"}, 404
    else:
        return "", 204
```

---

## 📄 Project Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/song-management-api.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables for MongoDB connection:
   - `MONGODB_SERVICE`: MongoDB service address.
   - `MONGODB_USERNAME`: MongoDB username (if applicable).
   - `MONGODB_PASSWORD`: MongoDB password (if applicable).
   - `MONGODB_PORT`: MongoDB port (default is usually 27017).

4. Run the Flask app:
   ```bash
   python app.py
   ```

The application will now be accessible at `http://localhost:5000`.

---

## 🧪 Testing the API

You can use the following `curl` commands to test the API endpoints:

- **Health check:**
  ```bash
  curl http://localhost:5000/health
  ```

- **Count the songs:**
  ```bash
  curl http://localhost:5000/count
  ```

- **Get all songs:**
  ```bash
  curl http://localhost:5000/song
  ```

- **Get a song by ID:**
  ```bash
  curl http://localhost:5000/song/{id}
  ```

- **Create a new song:**
  ```bash
  curl --request POST --header "Content-Type: application/json" --data '{"id": 101, "title": "New Song", "lyrics": "These are the lyrics."}' http://localhost:5000/song
  ```

- **Update a song by ID:**
  ```bash
  curl --request PUT --header "Content-Type: application/json" --data '{"title": "Updated Song", "lyrics": "Updated lyrics."}' http://localhost:5000/song/{id}
  ```

- **Delete a song by ID:**
  ```bash
  curl --request DELETE http://localhost:5000/song/{id}
  ```

---

## 📚 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👋 Contributing

If you'd like to contribute, feel free to fork the repository and open a pull request. Make sure to follow the guidelines and ensure all tests are passing before submitting your changes.

---

## 🎉 Enjoy using the Song Management API!

Happy coding! 🎶✨
