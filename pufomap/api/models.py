from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geomodels

from taggit.managers import TaggableManager


STATUS = (
    ("PUB","Publicada"),
    ("PEN","Pendiente"),
    ("INV","No válida"),
    )


class POI(models.Model):
    #author = models.ForeignKey('User', on_delete=models.SET(get_admin_user))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pois')
    name = models.CharField(max_length=200)
    location = geomodels.PointField(blank=False, null=True)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS, default="PEN")
    severity = models.IntegerField()
    tags = TaggableManager()
    created_date = models.DateTimeField(
            blank=True, null=False,
            auto_now_add=True
    )
    updated_date = models.DateTimeField(
            blank=True, null=True,
            auto_now=True,
    )
    ratings = models.ManyToManyField(User, related_name='userratings', through='Rating')
    comments = models.ManyToManyField(User, related_name='usercomments', through='Comment')

    @property
    def positive_ratings_count(self):
        return len(Rating.objects.filter(poi=self).filter(vote=1))

    @property
    def negative_ratings_count(self):
        return len(Rating.objects.filter(poi=self).filter(vote=-1))

    
    def __str__(self):
        return self.name


class POIImage(models.Model):
    poi = models.ForeignKey('POI', related_name='photos',
            on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='uploads',
            blank=False, null=False)


VOTES = (
    (1, 'Positivo'),
    (-1, 'Negativo'))


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_pois')
    poi = models.ForeignKey(POI, on_delete=models.CASCADE, related_name='poi_ratings')
    vote = models.IntegerField(choices=VOTES)

    def __str__(self):
        return "{} votó {} en {}".format(self.user, self.vote, self.poi)

    class Meta:
        unique_together = ("user", "poi")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_comments')
    poi = models.ForeignKey(POI, on_delete=models.CASCADE, related_name='poi_comments')
    comment = models.TextField()
    created_date = models.DateTimeField(
            blank=True, null=False,
            auto_now_add=True
    )

    def __str__(self):
        return "{} comentó {} en {}".format(self.user, self.comment, self.poi)
