from flask import Flask, jsonify, request

app = Flask(__name__)




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


# Support either Event objects or dictionary records.
def event_id(event):
    return event["id"] if isinstance(event, dict) else event.id


def event_title(event):
    return event["title"] if isinstance(event, dict) else event.title


def event_to_dict(event):
    if isinstance(event, dict):
        return {"id": event["id"], "title": event["title"]}
    return event.to_dict()


def set_event_title(event, title):
    if isinstance(event, dict):
        event["title"] = title
    else:
        event.title = title


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Event Management API"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event_to_dict(event) for event in events]), 200


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Valid JSON data is required"}), 400



    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    new_id = max((event_id(event) for event in events), default=0) + 1
    new_event = Event(new_id, title.strip())
    events.append(new_event)

    return jsonify(event_to_dict(new_event)), 201


@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Valid JSON data is required"}), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    for event in events:
        if event_id(event) == id:
            set_event_title(event, title.strip())
            return jsonify(event_to_dict(event)), 200

    return jsonify({"error": f"Event with ID {id} not found"}), 404






@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    for event in events:
        if event_id(event) == id:
            events.remove(event)
            return "", 204

    return jsonify({"error": f"Event with ID {id} not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
    
