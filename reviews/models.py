from django.db import models


class Review(models.Model):
    review_id = models.AutoField(primary_key=True, unique=True)
    user_id = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)

    info = models.TextField()
    created_date = models.DateField(null=False, blank=False)
    rate = models.PositiveSmallIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    pictures = models.CharField(max_length=40)
    #feedbacks_id_list = models.CharField(max_length=400)


class Product(models.Model):
    product_id = models.AutoField(primary_key=True, unique=True)
    url = models.URLField(max_length=200)
    site_name = models.CharField(max_length=20)
    product_type = models.CharField(max_length=40)


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True, unique=True)
    review_id = models.ForeignKey('Review', on_delete=models.CASCADE)
    user_id = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)

    info = models.TextField()
    rate = models.PositiveSmallIntegerField()
    date = models.DateField(null=False, blank=False)
