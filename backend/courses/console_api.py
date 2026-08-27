from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .console_serializers import ChapterAdminSerializer, CourseAdminSerializer, CourseDetailAdminSerializer, QuestionAdminSerializer
from .models import Chapter, Course, Question


class CourseAdminViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by("title")
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        return CourseDetailAdminSerializer if self.action == "retrieve" else CourseAdminSerializer


class ChapterAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ChapterAdminSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Multipart for file uploads, JSON for normal CRUD

    def get_queryset(self):
        qs = Chapter.objects.all().order_by("course", "order")
        course_id = self.request.query_params.get("course")
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs

    @action(detail=True, methods=['post'], url_path='upload-pdf')
    def upload_pdf(self, request, pk=None):
        """Upload a PDF file for a chapter"""
        chapter = self.get_object()
        serializer = self.get_serializer(chapter, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class QuestionAdminViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionAdminSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = Question.objects.all().prefetch_related("choices")
        course_id = self.request.query_params.get("course")
        chapter_id = self.request.query_params.get("chapter")
        if course_id:
            qs = qs.filter(course_id=course_id)
        if chapter_id:
            qs = qs.filter(chapter_id=chapter_id)
        return qs