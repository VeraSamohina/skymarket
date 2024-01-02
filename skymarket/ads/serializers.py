from rest_framework import serializers
from ads.models import Comment, Ad


class CommentSerializer(serializers.ModelSerializer):
    """
        Сериализатор модели Comment(Комментарии).
        Реализованы поля - имя и фамилия автора.
        """
    author_first_name = serializers.CharField(source="author.first_name", read_only=True)
    author_last_name = serializers.CharField(source="author.last_name", read_only=True)

    class Meta:
        model = Comment
        exclude = ('id', 'author')


class AdSerializer(serializers.ModelSerializer):
    """
        Сериализатор для отображения модели объявления

    """
    class Meta:
        model = Ad
        fields = ('pk', 'title', 'image', 'price', 'description')


class AdDetailSerializer(serializers.ModelSerializer):
    """
        Сериализатор для отображения детального вида объявления.
        Реализованы поля - имя, фамилия и электронная почта автора.
    """

    author_first_name = serializers.CharField(source="author.first_name", read_only=True)
    author_last_name = serializers.CharField(source="author.last_name", read_only=True)
    author_email = serializers.CharField(source="author.email", read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'
