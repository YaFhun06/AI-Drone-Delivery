from src.create_app import create_app
from src.extensions import socketio
from src.sockets import emit_order_update


app = create_app()

with app.app_context():
    client = socketio.test_client(app)

    print("Connected:", client.is_connected())

    client.emit(
        "join_order_room",
        {
            "order_id": 1
        }
    )

    emit_order_update(
        1,
        {
            "order_id": 1,
            "status": "COMPLETED"
        }
    )

    received = client.get_received()

    print("Received events:")
    print(received)