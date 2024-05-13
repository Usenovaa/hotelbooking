from typing import List, Tuple

from django.db import models


class Bookmark(models.Model):

    hotel = models.ForeignKey('hotel.Hotel', on_delete=models.CASCADE)
    user = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, related_name='bookmarks'
    )

    class Meta:

        ordering = ('-pk',)

        unique_together: List[Tuple[str, str]] = [
            ('hotel', 'user'),
        ]

        indexes: List[models.Index] = [
            models.Index(fields=('hotel', 'user')),
        ]
