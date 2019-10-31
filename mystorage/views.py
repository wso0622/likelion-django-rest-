from rest_framework import viewsets
from .models import Essay, Album,Files
from .serializers import EssaySerializer,AlbumSerializer,FilesSerializer
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer

    #검색기능
    filter_backends = [SearchFilter]
    search_fields = ('title','body')

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

    #현재 request를 보낸 유저
    # == self.request.user

    # 로그인 한 유저만 text를 볼 수 있게 하는 기능
    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated:
            qs = qs.filter(author = self.request.user)
        else:
            qs = qs.none()
        return qs

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

    #parser_class 지정(다양한 파일을 받아줌)
    parser_classes = (MultiPartParser, FormParser)
    
    #create() 오버라이딩 시키면 된다
    #API HTTP -> get() post()

    #create() -> post()
    def post(self,request, *args, **kargs):
        serializer = FilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)