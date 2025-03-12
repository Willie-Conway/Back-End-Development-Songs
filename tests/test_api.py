import json
import requests

def test_health(client):
    """Test the /health endpoint"""
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json == {"status": "OK"}

def test_get_songs(client):
    """Test the /song endpoint to get all songs"""
    # Make a GET request to the /song endpoint
    res = client.get("/song")
    
    # Assert that the response status code is 200 OK
    assert res.status_code == 200
    
    # Assert that the response contains a key "songs" and it's a list
    assert "songs" in res.json
    assert isinstance(res.json["songs"], list)
    
    # Optionally, check if the number of songs returned is as expected
    expected_song_count = 20  # Replace with the actual number of songs in your collection
    assert len(res.json["songs"]) == expected_song_count


def test_get_song_by_id(client):
    """Test the /song/<id> endpoint to get a song by id"""
    song_id = 1  # Replace with an actual song id in your database
    
    # Make a GET request to the /song/<id> endpoint
    res = client.get(f"/song/{song_id}")
    
    # Assert that the response status code is 200 OK
    assert res.status_code == 200
    
    # Assert that the response contains the song data and not an error message
    assert "id" in res.json
    assert res.json["id"] == song_id

def test_song_not_found(client):
    """Test that requesting a non-existent song returns 404"""
    non_existent_id = 999  # Replace with an ID that doesn't exist in your database
    
    # Make a GET request to the /song/<non_existent_id> endpoint
    res = client.get(f"/song/{non_existent_id}")
    
    # Assert that the response status code is 404 NOT FOUND
    assert res.status_code == 404
    
    # Assert that the response contains the correct error message
    assert res.json == {"message": f"song with id {non_existent_id} not found"}