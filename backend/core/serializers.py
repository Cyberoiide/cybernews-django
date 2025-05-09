from rest_framework import serializers
from .models import Article, Source

class ArticleSerializer(serializers.ModelSerializer):
    source = serializers.DictField()

    class Meta:
        model = Article
        fields = ['title', 'url', 'source', 'content', 'summary', 'tags', 'score']

    def validate_url(self, value):
        if Article.objects.filter(url=value).exists():
            raise serializers.ValidationError("Un article avec cette URL existe déjà.")
        return value

    def create(self, validated_data):
        source_data = validated_data.pop('source')
        source, _ = Source.objects.get_or_create(
            name=source_data['name'],
            defaults={
                'domain': source_data.get('domain'),
                'favicon': source_data.get('favicon'),
            }
        )
        return Article.objects.create(source=source, **validated_data)
