import uuid


class Node(object):
    def __init__(self):
        # node id format: node-{uuid}
        self.id = "node-" + uuid.uuid4()
        self.connections = []

    def get_sum_connections_weight(self):
        total = 0.0
        for conn in self.connections:
            total += conn.weight
        return total

    def add_connection(self, connection):
        self.connections.append(connection)
