from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ClientSerializer, ProjectSerializer, ClientDetailSerializer


def execute_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]


class ClientListView(APIView):
    def get(self, request):
        clients = execute_query("SELECT id, client_name, created_at, created_by FROM clients")
        return Response(clients, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        created_by = request.user.username
        query = "INSERT INTO clients (client_name, created_at, created_by) VALUES (%s, NOW(), %s) RETURNING id"
        client_id = execute_query(query, [data['client_name'], created_by])[0]['id']
        client = execute_query("SELECT * FROM clients WHERE id = %s", [client_id])[0]
        return Response(client, status=status.HTTP_201_CREATED)


class ClientDetailView(APIView):
    def get(self, request, id):
        client = execute_query("SELECT * FROM clients WHERE id = %s", [id])
        if not client:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        projects = execute_query("SELECT id, project_name FROM projects WHERE client_id = %s", [id])
        client_data = client[0]
        client_data['projects'] = projects
        return Response(client_data, status=status.HTTP_200_OK)

    def put(self, request, id):
        data = request.data
        execute_query("UPDATE clients SET client_name = %s, updated_at = NOW() WHERE id = %s",
                      [data['client_name'], id])
        client = execute_query("SELECT * FROM clients WHERE id = %s", [id])[0]
        return Response(client, status=status.HTTP_200_OK)

    def delete(self, request, id):
        execute_query("DELETE FROM clients WHERE id = %s", [id])
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectView(APIView):
    def post(self, request):
        data = request.data
        created_by = request.user.username
        query = "INSERT INTO projects (project_name, client_id, created_at, created_by) VALUES (%s, %s, NOW(), %s) RETURNING id"
        project_id = execute_query(query, [data['project_name'], data['client_id'], created_by])[0]['id']

        for user_id in data['users']:
            execute_query("INSERT INTO project_users (project_id, user_id) VALUES (%s, %s)", [project_id, user_id])

        project = execute_query("SELECT * FROM projects WHERE id = %s", [project_id])[0]
        project['users'] = execute_query("SELECT user_id FROM project_users WHERE project_id = %s", [project_id])
        return Response(project, status=status.HTTP_201_CREATED)


class UserProjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        projects = execute_query("SELECT p.id, p.project_name, c.client_name FROM projects p "
                                 "JOIN clients c ON p.client_id = c.id "
                                 "JOIN project_users pu ON p.id = pu.project_id "
                                 "WHERE pu.user_id = %s", [user_id])
        return Response(projects, status=status.HTTP_200_OK)


class ProjectDetailView(APIView):
    def delete(self, request, id):
        execute_query("DELETE FROM projects WHERE id = %s", [id])
        return Response(status=status.HTTP_204_NO_CONTENT)
