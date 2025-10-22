# Generated manually on 2025-10-10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_technews_featured_screen'),
    ]

    operations = [
        migrations.AddField(
            model_name='startupstory',
            name='featured_screen',
            field=models.JSONField(blank=True, default=dict, help_text='Featured screen configuration: {"url": "image/video URL", "type": "image/video", "is_featured": true/false}', null=True),
        ),
        migrations.AddField(
            model_name='sharxathon',
            name='featured_screen',
            field=models.JSONField(blank=True, default=dict, help_text='Featured screen configuration: {"url": "image/video URL", "type": "image/video", "is_featured": true/false}', null=True),
        ),
    ]
