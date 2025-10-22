# Generated manually on 2025-10-10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_neoproject_featured_screen'),
    ]

    operations = [
        migrations.AddField(
            model_name='technews',
            name='featured_screen',
            field=models.JSONField(blank=True, default=dict, help_text='Featured screen configuration: {"url": "image/video URL", "type": "image/video", "is_featured": true/false}', null=True),
        ),
    ]
