import time
from operator import truediv
from threading import Thread
from flask import Flask, render_template, Response, stream_with_context
from decode import initialize_kiss, located, received


def create_app():
    app = Flask(__name__)

    kiss_thread = Thread(target=initialize_kiss)
    kiss_thread.start()

    @app.route("/")
    def index():
        return render_template("map.html")

    @app.route("/stations")
    def stations():
        return list(located.values())

    @app.route("/packets")
    def broadcast():
        def stream():
            while True:
                message = received.get()
                print(message)
                yield f"data: {str(message)}\n\n"
        return Response(stream_with_context(stream()), content_type='text/event-stream')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)