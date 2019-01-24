import logging

from django.db import models
from django.utils.text import slugify
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
import requests

log = logging.getLogger(__name__)


CATEGORIES = {
    'A': 'metro',
    'B': 'local',
    'C': 'district',
}

class LocationNotFound(Exception):
    pass

class Geography(models.Model):
    #: The level for this geography (eg. `country`) which, together with
    #: `geo_code`, makes up the unique geo id.
    geo_level = models.CharField(max_length=15, null=False)
    #: The code for this geography which must be unique for this level.
    #: Together with `geo_level`, this makes up the unique geo id.
    geo_code = models.CharField(max_length=10, null=False)

    #: Name of this geography.
    name = models.CharField(max_length=100, null=False, db_index=True)
    #: Long name of this geography, giving it context (such as a city or province)
    #: If this is null, it is computed based on the place's ancestors.
    long_name = models.CharField(max_length=100, null=True, db_index=True)

    #: Area in square kilometers. Optional.
    square_kms = models.FloatField(null=True)

    # hierarchy
    #: The level of this geography's parent, or `None` if this is the root
    #: geography that has no parent.
    parent_level = models.CharField(max_length=15, null=True)
    #: The code of this geography's parent, or `None` if this is the root
    #: geography that has no parent.
    parent_code = models.CharField(max_length=10, null=True)

    province_name = models.CharField(max_length=100, null=False)
    province_code = models.CharField(max_length=5, null=False)
    category = models.CharField(max_length=2, null=False)
    miif_category = models.TextField(null=True)
    population = models.IntegerField(null=True)

    class Meta:
        unique_together = ('geo_level', 'geo_code')
        verbose_name_plural = "geographies"

    @property
    def category_name(self):
        return CATEGORIES[self.category] + ' municipality'

    @property
    def geoid(self):
        return '-'.join([self.geo_level, self.geo_code])

    @property
    def slug(self):
        return slugify(self.name)

    @property
    def parent_geoid(self):
        if self.parent_level and self.parent_code:
            return '%s-%s' % (self.parent_level, self.parent_code)
        return None

    @property
    def parent(self):
        """ The parent of this geograhy, or `None` if this is the root of
        the hierarchy.
        """
        if not hasattr(self, '_parent'):
            if self.parent_level and self.parent_code:
                self._parent = self.__class__.objects.filter(geo_level=self.parent_level, geo_code=self.parent_code).first()
            else:
                self._parent = None

        return self._parent

    def ancestors(self):
        """ A list of the ancestors of this geography, all the way up to the root.
        This is an empty list if this geography is the root of the hierarchy.
        """
        ancestors = []
        g = self.parent
        while g:
            ancestors.append(g)
            g = g.parent
        return ancestors

    def as_dict(self):
        return {
            'full_geoid': self.geoid,
            'full_name': self.long_name,
            'name': self.long_name,
            'short_name': self.name,
            'geo_level': self.geo_level,
            'geo_code': self.geo_code,
            'parent_geoid': self.parent_geoid,
            'square_kms': self.square_kms,
            'province_name': self.province_name,
            'province_code': self.province_code,
            'category': self.category,
            'category_name': self.category_name,
            'miif_category': self.miif_category,
            'slug': self.slug,
        }

    def __unicode__(self):
        return self.long_name

    def __str__(self):
        return self.__unicode__()

    @classmethod
    def find(cls, geo_code, geo_level):
        geo = cls.objects.filter(geo_level=geo_level, geo_code=geo_code).first()
        if not geo:
            raise LocationNotFound("Invalid level, code: %s-%s" % (geo_level, geo_code))
        return geo

    @classmethod
    def get_locations_from_coords(cls, revgeocoder, longitude, latitude):
        geos = []
        for geo_code, geo_level in revgeocoder.lookup(longitude, latitude):
            try:
                geo = cls.find(geo_code, geo_level.lower())

                if geo.geo_level in ['municipality', 'district']:
                    geos.append(geo)
            except LocationNotFound as e:
                log.warn("Couldn't find geo that Mapit gave us: %s %s" % (geo_code, geo_level), exc_info=e)

        return geos

class Programme(models.Model):
    name = models.CharField(max_length=20, null=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

class Project(models.Model):
    STATUS = (
        ("Planned", 'Planned'),
        ("Preparation", 'In preparation'),
        ("Implementation", 'Implementation'),
        ("Closing", 'Documentation & Closing'),
    )

    geo = models.ForeignKey(Geography, on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme, null=False)
    title = models.CharField(max_length=255, null=False)
    status = models.CharField(choices=STATUS, null=False, max_length=255)
    area_of_work = models.CharField(blank=True, max_length=255, null=True)
    mode_of_delivery = models.CharField(blank=True, max_length=255, null=True)
    partner = models.CharField(blank=True, max_length=255, null=True)
    supported_policies = models.CharField(blank=True, max_length=255, null=True)
    m_and_e = models.CharField(blank=True, max_length=255, null=True, verbose_name="M & E")
    contact = models.CharField(blank=True, max_length=255, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.geo)

class CleanForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row, *args, **kwargs):
        if hasattr(value, "strip"):
            value = value.strip()
        return super(CleanForeignKeyWidget, self).clean(value, row, *args, **kwargs)

class ProjectResource(resources.ModelResource):
    programme = Field(
        column_name='programme',
        attribute='programme',
        widget=CleanForeignKeyWidget(Programme, 'name')
    )

    geo = Field(
        column_name='municipality',
        attribute='geo',
        widget=CleanForeignKeyWidget(Geography, 'geo_code')
    )

    class Meta:
        model = Project
        export_order = (
            'id', 'programme', 'geo', 'title', 'status', 
            'area_of_work', 'mode_of_delivery', 'partner',
            'supported_policies', 'm_and_e', 'contact',
        )
