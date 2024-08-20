from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer,
                                                  CourseExampleSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course, Group
from users.models import Subscription, Balance


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        group = Group.objects.filter(course=course)
        return group


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы"""

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        user_balance = Balance.objects.get(user_id=self.request.user.pk)
        product_price = request.data['product_price']
        data = dict()

        if user_balance.balance < product_price:
            return Response(
                data={'error': 'insufficient funds in the account'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user_balance.balance = user_balance - product_price
            user_balance.save()

        data.update({'user_balance': user_balance.balance})

        Subscription.objects.create(course_id=pk, user_id=user_balance.user_id)

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )


class CourseExampleViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return CourseExampleSerializer

    def get_queryset(self):
        sub_data = Subscription.objects.filter(user_id=self.request.user.pk).values('course_id')
        return Course.objects.exclude(pk__in=sub_data)
