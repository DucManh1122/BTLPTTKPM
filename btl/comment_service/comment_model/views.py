
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Comment
from .serializer import CommentSerializer

# Create your views here.
@api_view(['GET'])
def comment_list(request):
    product_id = request.query_params.get('Product ID')
    comments = Comment.objects.filter(product_id=product_id)
    if comments:
        serializer = CommentSerializer(comments,many=True)
        return Response({"status": "success","data": serializer.data}, status=status.HTTP_200_OK)
    return Response({"status":"failed","message":"Chưa có bình luận cho sản phẩm"})


@api_view(['POST'])
def add_comment(request):
    data = {
        'username' : request.data.get('Username'),
        'product_id' : request.data.get('Product ID'),
        'content' : request.data.get('Content'),
    }
    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        serializer.create(data)
        return Response({"status":"Success","message":"Comment is added Successfully.","data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    