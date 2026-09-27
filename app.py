from flask import Flask, jsonify, request

app = Flask(__name__)
 
@app.route("/")
def home():
    return "Flask API is running!"
    
# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    title = data.get("title")
    if not title:
        return jsonify({"error": "The 'title' field is required"}), 400

    new_id = max([event.id for event in events], default=0) + 1

    new_event = Event(new_id, title)
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    # Return 404 if the requested event does not exist
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    # Only update the title
    if "title" not in data:
        return jsonify({"error": "The 'title' field is required"}), 400

    event.title = data["title"]

    return jsonify(event.to_dict()), 200

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    # Return 404 if the requested event does not exist
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)

    return jsonify({
        "message": "Event deleted successfully",
        "event": event.to_dict()
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
