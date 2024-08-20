from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from rest_framework import serializers

from courses.models import Course, Group, Lesson
from users.models import Subscription

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    class Meta:
        model = Group
        fields = '__all__'


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = ('title', )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons(self, obj):
        data = Lesson.objects.filter(course_id=obj.pk).values('title')
        serializer = MiniLessonSerializer(data, many=True)
        return serializer.data

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return Lesson.objects.filter(course_id=obj.pk).count()

    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""
        return Group.objects.filter(course_id=obj.pk).count()

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум 30 чел.."""
        return int((Group.objects.filter(course_id=obj.pk).count() / 30) * 100)

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        st_group = Group.objects.filter(course_id=obj.pk).count()
        st_sub = Subscription.objects.filter(course_id=obj.pk).count()

        try:
            return int((st_sub / st_group) * 100)
        except ZeroDivisionError:
            return 0

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
            'lessons',
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = '__all__'


class CourseExampleSerializer(serializers.ModelSerializer):

    lessons_count = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, instance):
        return Lesson.objects.filter(course_id=instance.pk).count()

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count'
        )
