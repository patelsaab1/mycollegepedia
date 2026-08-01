from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class TimeStamp(models.Model):
    created_at = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = 'TimeStamp'
        verbose_name_plural = 'TimeStamps'
        abstract = True

class Religion(models.Model):
    name = models.CharField(max_length=100, verbose_name='Religion name')

    class Meta:
        verbose_name = 'Religion'
        verbose_name_plural = 'Religions'
        ordering = ["name"]
        
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Category name')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ["name"]
    def __str__(self):
        return self.name
        
class Country(models.Model):
    name = models.CharField(max_length=100)


    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ["name"]
        
    def __str__(self):
        return self.name
        
class State(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'
        ordering = ["name","country"]

    def __str__(self):
        return self.name


class Address(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    city = models.CharField(_("city"), max_length=70)
    current_address = models.TextField(_("current address"),blank=True)
    permanent_address = models.TextField(_("permanent address"),blank=True)
    zipcode = models.IntegerField(_("zipcode"), null=True, )

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Address'
        abstract = True
    
class SEO(models.Model):
    meta_title = models.CharField(verbose_name='meta title', max_length=200, blank=True, null=True)
    meta_keyword = models.TextField(verbose_name='meta keywords', blank=True, null=True)
    meta_description = models.TextField(verbose_name='meta description', blank=True, null=True)

    class Meta:
        verbose_name = 'SEO'
        verbose_name_plural = 'SEO'
        abstract = True

class SocialMedia(models.Model):
    primary_mobile = models.CharField(verbose_name="primary mobile number", max_length=15,help_text="mobile number must be entered in the format: '+911234567890'.",blank=True,null=True)
    secondary_mobile = models.CharField(verbose_name="secondary mobile number", max_length=15,help_text="mobile number must be entered in the format: '+911234567890'.",blank=True,null=True)
    email = models.EmailField(verbose_name='email', max_length=255,blank=True,null=True)
    website = models.URLField(verbose_name='website url', blank=True, null=True)
    whatsapp = models.URLField(verbose_name='whatsapp url', blank=True, null=True)
    facebook = models.URLField(verbose_name='facebook url', blank=True, null=True)
    instagram = models.URLField(verbose_name='instagram url', blank=True, null=True)
    linkedin = models.URLField(verbose_name='linkedin url', blank=True, null=True)
    twitter = models.URLField(verbose_name='twitter url', blank=True, null=True)
    youtube = models.URLField(verbose_name='youtube url', blank=True, null=True)
    telegram = models.URLField(verbose_name='telegram url', blank=True, null=True)
    website = models.URLField(verbose_name='website url', blank=True, null=True)

    class Meta:
        verbose_name = 'SocialMedia'
        verbose_name_plural = 'SocialMedia'
        abstract = True