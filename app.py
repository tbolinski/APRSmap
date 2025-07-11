from threading import Thread
from flask import Flask, render_template, Response, stream_with_context
import database
from decode import initialize_kiss, located, received, moved
import json

def create_app():
    database.create_db()

    app = Flask(__name__)

    kiss_thread = Thread(target=initialize_kiss)
    kiss_thread.start()

    @app.route("/")
    def index():
        return render_template("map.html")

    @app.route("/stations")
    def stations():
        return list(located.values())

    @app.route("/locations")
    def locations():
        def stream():
            while True:
                new_loc = moved.get()
                yield f"data: {json.dumps(new_loc)}\n\n"
        return Response(stream_with_context(stream()), content_type='text/event-stream')

    @app.route("/packets")
    def broadcast():
        def stream():
            while True:
                message = received.get()
                print(message)
                yield f"data: {json.dumps(message)}\n\n"
        return Response(stream_with_context(stream()), content_type='text/event-stream')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)