from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tasks.serializers import TaskSerializer
from tasks.models import Task


# Create your views here.

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'all_items': '/get_tasks',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }
    return Response(api_urls)

@api_view(['POST'])
def add_task(request):
    try:
        if Task.objects.filter(**request.data).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST, data="This note already exists")
        task = TaskSerializer(data=request.data)
        if task.is_valid():
            task.save()
            return Response(task.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Invalid Data")
    except ValidationError:
        return Response(status=status.HTTP_400_BAD_REQUEST, data="Invalid Data" )

@api_view(['GET'])
def get_tasks(request):
    if request.query_params:
        tasks = Task.objects.filter(**request.query_params.dict())
    else:
        tasks = Task.objects.all()

    if tasks:
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        data = TaskSerializer(instance=task, data=request.data)

        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Invalid Data")
    except Task.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST, data="This note doesn`t exist")

@api_view(['DELETE'])
def delete_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data="Successfully deleted")
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data="This note doesn`t exist")