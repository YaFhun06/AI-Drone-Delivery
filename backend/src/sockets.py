def register_socket_events(socketio):
    @socketio.on("connect")
    def handle_connect():
        print("Client connected")

    @socketio.on("disconnect")
    def handle_disconnect():
        print("Client disconnected")

    @socketio.on("join_order_room")
    def handle_join_order_room(data):
        from flask_socketio import join_room
        order_id = data.get("order_id")
        if order_id:
            join_room(f"order_{order_id}")

    @socketio.on("join_customer_room")
    def handle_join_customer_room(data):
        from flask_socketio import join_room
        customer_id = data.get("customer_id")
        if customer_id:
            join_room(f"customer_{customer_id}")


def emit_order_update(order_id, payload):
    from src.extensions import socketio
    socketio.emit("order_status_updated", payload, room=f"order_{order_id}")


def emit_notification(customer_id, payload):
    from src.extensions import socketio
    socketio.emit("new_notification", payload, room=f"customer_{customer_id}")