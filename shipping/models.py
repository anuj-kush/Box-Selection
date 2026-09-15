from django.db import models
from django.core.validators import MinValueValidator

class Dimensions(models.Model):
    name = models.CharField(max_length=120, unique=True)
    length_mm = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    width_mm = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    height_mm = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        abstract = True
        constraints = [models.CheckConstraint(condition=models.Q(length_mm__gt=0, width_mm__gt=0, height_mm__gt=0), name="%(class)s_positive_dimensions")]

    @property
    def dimensions(self):
        return (self.length_mm, self.width_mm, self.height_mm)

    def __str__(self):
        return self.name

class Product(Dimensions):
    weight_g = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta(Dimensions.Meta):
        abstract = False
        constraints = Dimensions.Meta.constraints + [models.CheckConstraint(condition=models.Q(weight_g__gt=0), name="product_positive_weight")]

class Box(Dimensions):
    max_weight_g = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    active = models.BooleanField(default=True)

    class Meta(Dimensions.Meta):
        abstract = False
        constraints = Dimensions.Meta.constraints + [models.CheckConstraint(condition=models.Q(max_weight_g__gt=0, cost__gte=0), name="box_valid_weight_cost")]
