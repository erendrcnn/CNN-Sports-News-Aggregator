# Generated migration for NewsArticle model

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('link', models.URLField(max_length=1000, unique=True)),
                ('published_date', models.DateTimeField()),
                ('description', models.TextField(blank=True)),
                ('source', models.CharField(default='CNN Sports', max_length=100)),
                ('guid', models.CharField(max_length=500, unique=True)),
                ('fetched_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-published_date'],
                'indexes': [
                    models.Index(fields=['-published_date'], name='news_newsar_publish_idx'),
                    models.Index(fields=['source'], name='news_newsar_source_idx'),
                ],
            },
        ),
    ]
