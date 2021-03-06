from django.db import models
# ImageKit
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit

class Posting(models.Model):
    content = models.TextField(default='')
    icon = models.CharField(max_length=20, default='fas fa-question')

    # 원본 유지 저장
    # upload URL => /media/posting/origin/그날날짜
    # image = models.ImageField(blank=True, upload_to='posting/origin/%Y%m%d')

    # resize된 이미지 저장
    image = ProcessedImageField(
        upload_to='posting/resize/%Y%m%d',
        processors=[ResizeToFit(width=960, upscale=False)], # 크면 960으로줄이는데, 작은게 들어오면 늘리진 X
        format='JPEG',
    )

    # thumbnail
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=320, upscale=False)],
        format='JPEG',
        options={'quality':60},  # 원본 퀄리티의 60%
    )


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} : {self.content[:20]}'

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        print()
        print(f'==== Save Posting with id : {self.id} ===')
        print(f'     content: {self.content}')
        if self.image:
            print(f'     image_size: {self.image.width}px * {self.image.height}px : {round(self.image.size / 1024)}kb')
        print('============================================')

class Comment(models.Model):
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.posting.content[:10]} : {self.content[:20]}'