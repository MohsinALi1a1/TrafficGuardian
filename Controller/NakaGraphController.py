from flask import jsonify
from collections import defaultdict, deque
from Model.NakaGraph import NakaGraph
from Model.Configure import db




class NakaGraphController:

    @staticmethod
    def get_next_hops(naka_id, max_hops):
        graph = NakaGraphController.build_graphoneway_from_db()
        # graph = NakaGraphController.build_graph_from_db() #For 2 way Graph
        queue = deque([(naka_id, 0)])
        visited = set()
        hops = defaultdict(list)

        while queue:
            current, depth = queue.popleft()

            if current in visited:
                continue
            visited.add(current)

            if 1 <= depth <= max_hops:
                hops[depth].append(current)

            if depth < max_hops:
                for neighbor in graph.get(current, []):
                    if neighbor not in visited:
                        queue.append((neighbor, depth + 1))

        return jsonify({
            "FromNakaID": naka_id,
            "Hops": dict(hops)
        }), 200

    @staticmethod
    def get_next_hops_only(naka_id):
        graph = NakaGraphController.build_graphoneway_from_db()
        next_hops = graph.get(naka_id, [])  # Returns list of connected ToNakaIDs
        return jsonify({
            'NakaID': naka_id,
            'NextHops': next_hops
        }), 200

# Build Graph one way
    @staticmethod
    def build_graphoneway_from_db():
        graph = defaultdict(list)
        connections = NakaGraph.query.all()
        for conn in connections:
            graph[conn.FromNakaID].append(conn.ToNakaID)  # Only one direction
        return dict(graph)

#Build Graph 2 Way
    @staticmethod
    def build_graph_from_db():
        graph = defaultdict(list)
        connections = NakaGraph.query.all()
        for conn in connections:
            graph[conn.FromNakaID].append(conn.ToNakaID)
            graph[conn.ToNakaID].append(conn.FromNakaID)  # Two-way connection
        return dict(graph)

#Algorithm of BEst for Search
    @staticmethod
    def bfs_alert(graph, start, max_hops):
        queue = deque([(start, 0)])
        visited = set()
        alert_list = []

        while queue:
            node, depth = queue.popleft()
            if depth > max_hops or node in visited:
                continue
            visited.add(node)
            if depth > 0:
                alert_list.append(node)
            for neighbor in graph.get(node, []):
                queue.append((neighbor, depth + 1))

        return alert_list


    @staticmethod
    def load_graph_and_alerts(start, max_hops):
        # Build the graph from the database
        # graph = NakaGraphController.build_graph_from_db()
        graph=NakaGraphController.build_graphoneway_from_db()

        # Get the alerts based on BFS
        alert_list = NakaGraphController.bfs_alert(graph, start, max_hops)

        # Return the graph and alerts as a response
        return {
            'graph': graph,
            'alerts': alert_list
        }


    @staticmethod
    def get_naka_by_id(id):
        """Fetch a specific Naka connection by ID."""
        naka = NakaGraph.query.get(id)
        if not naka:
            return jsonify({'error': 'Naka not found'}), 404
        return jsonify({
            'ID': naka.ID,
            'FromNakaID': naka.FromNakaID,
            'ToNakaID': naka.ToNakaID,
            'DistanceKM': naka.DistanceKM
        }), 200


    @staticmethod
    def add_connection(from_id, to_id_list, distance_list):
        """Add multiple Naka connections to the DB."""
        try:
            if len(to_id_list) != len(distance_list):
                return {'error': 'ToNakaID and DistanceKM lists must be of the same length'}, 400

            for to_id, distance in zip(to_id_list, distance_list):
                naka = NakaGraph(FromNakaID=from_id, ToNakaID=to_id, DistanceKM=distance)
                db.session.add(naka)

            db.session.commit()
            return {'message': 'Naka connections added successfully'}, 201

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return {'error': str(e)}, 500

    @staticmethod
    def get_all_connections():
        """Fetch all Naka connections from the DB."""
        naka_graphs = NakaGraph.query.all()
        result = [{
            'ID': naka.ID,
            'FromNakaID': naka.FromNakaID,
            'ToNakaID': naka.ToNakaID,
            'DistanceKM': naka.DistanceKM
        } for naka in naka_graphs]
        return jsonify(result), 200

    @staticmethod
    def update_connection(id, from_id, to_id, distance):
        """Update a specific Naka connection."""
        naka = NakaGraph.query.get(id)
        if not naka:
            return jsonify({'error': 'Naka connection not found'}), 404
        try:
            naka.FromNakaID = from_id
            naka.ToNakaID = to_id
            naka.DistanceKM = distance
            db.session.commit()
            return jsonify({'message': 'Naka connection updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @staticmethod
    def delete_connection(nakaid, tonaka):
        """Delete a specific Naka connection."""
        try:
            # Fetch the specific connection based on FromNakaID and ToNakaID
            naka = db.session.query(NakaGraph).filter(
                (NakaGraph.FromNakaID == nakaid) & (NakaGraph.ToNakaID == tonaka)
            ).first()

            if not naka:
                return {'error': 'Naka connection not found'}, 404

            db.session.delete(naka)
            db.session.commit()
            return {'message': 'Naka connection deleted successfully'}, 200

        except Exception as e:
            print(str(e))
            return {'error': str(e)}, 400



    @staticmethod
    def get_naka_graph_for_flutter():
        naka_graphs = NakaGraph.query.all()

        nodes = set()
        edges = []

        for naka in naka_graphs:
            from_id = naka.FromNakaID
            to_id = naka.ToNakaID

            nodes.add(from_id)
            nodes.add(to_id)

            edges.append({
                "from": from_id,
                "to": to_id
            })

        return jsonify({
            "nodes": list(nodes),
            "edges": edges
        }), 200
