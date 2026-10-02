from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    # Make sure JSON data was provided
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    # Make sure the title was provided
    title = data.get("title")

    if not title:
        return jsonify({"error": "Event title is required"}), 400

    # Generate a new ID based on the existing events
    new_id = max((event.id for event in events), default=0) + 1

    # Create and store the new event
    new_event = Event(new_id, title)
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update the title of an event
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    # Find the event with the requested ID
    event = next((event for event in events if event.id == id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Update only the title
    title = data.get("title")

    if not title:
        return jsonify({"error": "Event title is required"}), 400

    event.title = title

    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    # Find the event with the requested ID
    event = next((event for event in events if event.id == id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Remove the event from the in-memory list
    events.remove(event)

    return jsonify({
        "message": "Event deleted successfully",
        "event": event.to_dict()
    }), 200


if __name__ == "__main__":
    app.run(debug=True)

