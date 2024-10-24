from django.contrib import admin
from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Badge(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to="badges", null=True)

    def __str__(self) -> str:
        return self.name


class Rating(models.Model):
    name = models.CharField(max_length=200)
    short_desc = models.CharField(
        max_length=400, verbose_name="short description"
    )

    def __str__(self) -> str:
        return self.name


class Company(models.Model):
    class Meta:
        verbose_name_plural = "companies"

    name = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return self.name

    @admin.display(
        boolean=True,
        description="AC",
    )
    def animal_cruelty(self) -> bool:
        return self.categories.filter(name="Animal Cruelty").exists()

    @admin.display(
        boolean=True,
        description="EH",
    )
    def environmental_harm(self) -> bool:
        return self.categories.filter(name="Environmental Harm").exists()

    @admin.display(
        boolean=True,
        description="FF",
    )
    def fossil_fuels(self) -> bool:
        return self.categories.filter(name="Fossil Fuels").exists()

    @admin.display(
        boolean=True,
        description="HR",
    )
    def human_rights_violations(self) -> bool:
        return self.categories.filter(name="Human Rights Violations").exists()

    @admin.display(
        boolean=True,
        description="SH",
    )
    def social_harm(self) -> bool:
        return self.categories.filter(name="Social Harm").exists()

    @admin.display(
        boolean=True,
        description="W",
    )
    def weapons(self) -> bool:
        return self.categories.filter(name="Weapons").exists()


class Fund(models.Model):
    name = models.CharField(max_length=200)
    companies = models.ManyToManyField(Company, through="Holding", blank=True)
    returns = models.FloatField(null=True, blank=True)
    fees = models.FloatField(null=True, blank=True)
    badges = models.ManyToManyField(Badge, blank=True)
    ratings = models.ManyToManyField(Rating, through="FundRating")

    def __str__(self) -> str:
        return self.name

    def get_score(self, category: str) -> float:
        return self.companies.filter(
            holding__company__categories__name=category
        ).aggregate(total=models.Sum("holding__percentage", default=0))[
            "total"
        ]

    def get_all_scores(self) -> dict[Category, float]:
        return {
            cat: self.get_score(cat.name)
            for cat in Category.objects.order_by("name")
        }

    @property
    @admin.display(
        description="AC",
    )
    def animal_cruelty_score(self) -> float:
        return self.get_score("Animal Cruelty")

    @property
    @admin.display(
        description="EH",
    )
    def environmental_harm_score(self) -> float:
        return self.get_score("Environmental Harm")

    @property
    @admin.display(
        description="FF",
    )
    def fossil_fuels_score(self) -> float:
        return self.get_score("Fossil Fuels")

    @property
    @admin.display(
        description="HR",
    )
    def human_rights_violations_score(self) -> float:
        return self.get_score("Human Rights Violations")

    @property
    @admin.display(
        description="SH",
    )
    def social_harm_score(self) -> float:
        return self.get_score("Social Harm")

    @property
    @admin.display(
        description="W",
    )
    def weapons_score(self) -> float:
        return self.get_score("Weapons")


class Holding(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    percentage = models.FloatField()

    def __str__(self) -> str:
        return self.company.name


class FundRating(models.Model):
    class Score(models.TextChoices):
        A = "A"
        B = "B"
        C = "C"
        D = "D"
        E = "E"
        F = "F"

    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    score = models.CharField(
        max_length=1, choices=Score.choices, null=True, blank=True
    )
