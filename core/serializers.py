from rest_framework import serializers


class ClientSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    client_name = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.CharField(max_length=100, read_only=True)


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    project_name = serializers.CharField(max_length=100)
    client_id = serializers.IntegerField()
    users = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.CharField(read_only=True)


class ClientDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    client_name = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
