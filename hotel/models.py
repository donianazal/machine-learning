from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from picklefield.fields import PickledObjectField


class Hotel(models.Model):
    """Declaration of the Hotel object."""

    name = models.CharField(max_length=255)

    rating = models.FloatField(default=0.0)  # calculated recurrently, normalized
    avg_members_per_stay = models.FloatField(default=0.0)  # calculated recurrently
    avg_nights_per_stay = models.FloatField(default=0.0)  # calculated recurrently

    residences = models.IntegerField(default=0)

    nights = models.IntegerField(default=0)

    data_1 = PickledObjectField(blank=True, null=True)

    def __repr__(self):
        return f'<Hotel: {self.name}>'

    def __str__(self):
        return f'{self.name}'

    def reviews_count(self):
        return self.reviews.count()

    def get_absolute_url(self):
        return reverse('hotel-detail', kwargs={
            'pk': self.pk,
        })

    def get_rating_5(self):
        return round(self.rating * 5.0, 1)

    # used by management command
    def calculate_average_rating(self):
        """
        finds out the average rating for this hotel, caches the value in self.rating
        :return: average rating
        """
        # average = sum(map(lambda x: x.normalized_rating(), self.reviews)) / self.reviews_count()
        total_nights = self.reviews.aggregate(models.Sum('nights'))
        total_nights = total_nights['nights__sum']

        total_members = self.reviews.aggregate(models.Sum('members'))
        total_members = total_members['members__sum']

        query = self.reviews.all()
        nights_weighted_average = sum(
            map(lambda x: (x.normalized_rating() * float(x.nights) / float(total_nights)), query))

        # now take into account the members weight
        members_weighted_average = sum(
            map(lambda x: (x.normalized_rating() * float(x.members) / float(total_members)), query))
        self.rating = (nights_weighted_average + members_weighted_average) / 2.0
        # self.save()
        return self.rating

    def calculate_residences(self):
        residences = self.reviews.aggregate(models.Sum('members'))
        self.residences = residences['members__sum']
        # self.save()

    def calculate_nights(self):
        nights = self.reviews.aggregate(models.Sum('nights'))
        self.nights = nights['nights__sum']
        # self.save()

    def calculate_average_members_per_stay(self):
        query = self.reviews.all()
        stays = self.reviews.count()  # same number as reviews (each review record is a stay)
        average_members_per_stay = sum(
            map(lambda x: (float(x.members) / float(stays)), query))
        self.avg_members_per_stay = round(average_members_per_stay, 1)
        # self.save()

    def calculate_average_nights_per_stay(self):
        query = self.reviews.all()
        stays = self.reviews.count()  # same number as reviews (each review record is a stay)
        average_nights_per_stay = sum(
            map(lambda x: (float(x.nights) / float(stays)), query))
        # self.avg_nights_per_stay = round(average_nights_per_stay, 1)
        self.avg_nights_per_stay = round(average_nights_per_stay, 1)
        # self.save()

    def plot_membercount_avgrating(self):
        data = {}
        member_counts_list = self.reviews.order_by('members').values_list('members').distinct()
        for number_of_members in member_counts_list:
            number_of_members = number_of_members[0]  # since these are stored like a tuple from values_list
            reviews = self.reviews.filter(members=number_of_members)  # for that group
            avg_rating = reviews.aggregate(models.Avg('rating'))
            data[number_of_members] = round(avg_rating['rating__avg'], 2)
        self.data_1 = data
        return data


class Review(models.Model):
    rating = models.SmallIntegerField(verbose_name="Rating", blank=False, null=False)
    review_text = models.TextField(verbose_name="Review text", blank=False)
    hotel = models.ForeignKey(Hotel, related_name='reviews', on_delete=models.CASCADE)
    nights = models.SmallIntegerField(verbose_name="Nights", blank=False, null=False, default=1)
    members = models.SmallIntegerField(verbose_name="Members", blank=False, null=False, default=1)

    def __repr__(self):
        return f'<Review: {self.rating}>'

    def __str__(self):
        return f'{self.rating}'

    # for prototyping only
    def get_ratings_range(self):
        return range(0, self.rating)

    def normalized_rating(self):
        ratingf = float(self.rating)
        return (ratingf - 1.0) / (5.0 - 1.0)


class Post(models.Model):
    text = models.TextField(verbose_name="Post text")
    likes = models.IntegerField(verbose_name="Likes", default=0)

    def __repr__(self):
        return f'<Post: {self.text}>'

    def __str__(self):
        return f'{self.text}'
