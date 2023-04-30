from django.db import models
from django.contrib import admin


class Idgen(models.Model):
    nextval = models.IntegerField()

    class Meta:
        db_table = "idgen"


class IdgenAdmin(admin.ModelAdmin):
    fields = ["nextval"]
    list_display = ("nextval",)
    exclude = ["id"]


class Leagues(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "leagues"
        verbose_name = "League"
        verbose_name_plural = "Leagues"

    def __str__(self):
        return f"{self.name}"


class LeaguesAdmin(admin.ModelAdmin):
    fields = ["name"]
    # list_display = ('name')


class Divisions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    leagueid = models.ForeignKey(
        Leagues, on_delete=models.CASCADE, db_column="leagueid", default=0
    )

    class Meta:
        db_table = "divisions"
        verbose_name = "Division"
        verbose_name_plural = "Divisions"

    def __str__(self):
        return f"{self.name}"


class DivisionsAdmin(admin.ModelAdmin):
    fields = ["name", "leagueid"]
    list_display = ("name", "leagueid")


class Members(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    streetaddress1 = models.CharField(max_length=255)
    streetaddress2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)

    class Meta:
        db_table = "members"
        verbose_name = "Member"
        verbose_name_plural = "Members"

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Phonenumbers(models.Model):
    id = models.AutoField(primary_key=True)
    memberid = models.ForeignKey(
        Members, on_delete=models.CASCADE, db_column="memberid", default=0
    )
    phonenumber = models.CharField(max_length=25)
    workorhome = models.CharField(max_length=2)

    class Meta:
        db_table = "phonenumbers"
        verbose_name = "Phone Number"
        verbose_name_plural = "Phone Numbers"
        constraints = [
            models.UniqueConstraint(
                fields=["memberid", "phonenumber"], name="unique_phonenumber"
            ),
        ]

    def __str__(self):
        return f"{self.phonenumber}"


class PhonenumbersInline(admin.TabularInline):
    model = Phonenumbers
    extra = 0


class Emailaddresses(models.Model):
    id = models.AutoField(primary_key=True)
    memberid = models.ForeignKey(
        Members, on_delete=models.CASCADE, db_column="memberid", default=0
    )
    address = models.CharField(max_length=64)
    primaryaddress = models.CharField(max_length=2)

    class Meta:
        db_table = "emailaddresses"
        verbose_name = "Email Address"
        verbose_name_plural = "Email Addresses"
        constraints = [
            models.UniqueConstraint(
                fields=["memberid", "primaryaddress"], name="unique_primaryaddress"
            ),
        ]

    def __str__(self):
        return f"{self.address}"


class EmailaddressesInline(admin.TabularInline):
    model = Emailaddresses
    extra = 0


class MembersAdmin(admin.ModelAdmin):
    inlines = [PhonenumbersInline, EmailaddressesInline]
    fields = ["firstname", "lastname", "streetaddress1", "city", "state", "zipcode"]
    list_display = (
        "firstname",
        "lastname",
        "streetaddress1",
        "city",
        "state",
        "zipcode",
    )
    search_fields = ["lastname"]


class MembersAdmin(admin.ModelAdmin):
    inlines = [PhonenumbersInline, EmailaddressesInline]
    fields = ["firstname", "lastname", "streetaddress1", "city", "state", "zipcode"]
    list_display = (
        "firstname",
        "lastname",
        "streetaddress1",
        "city",
        "state",
        "zipcode",
    )
    search_fields = ["lastname"]


class Teams(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    memberid = models.ForeignKey(
        Members,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        db_column="memberid",
        default=0,
    )
    predecessor = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["city", "nickname"]
        db_table = "teams"
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return f"{self.city} {self.nickname}"


MONTH_CHOICES = (
    (5, "May"),
    (6, "Jun"),
    (7, "Jul"),
    (8, "Aug"),
    (9, "Sept"),
    (10, "Oct"),
    (11, "Nov"),
    (12, "Dec"),
    (13, "Jan"),
)

MONTHIDX_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
)


class TeamsAdmin(admin.ModelAdmin):
    fields = ["id", "city", "nickname", "memberid", "predecessor"]
    list_display = ("id", "city", "nickname", "memberid", "predecessor")
    search_fields = ["memberid", "city"]


class Schedules(models.Model):
    year = models.IntegerField()
    hometeam = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE,
        db_column="hometeam",
        related_name="schedules_hometeam_set",
        default=0,
    )
    visitteam = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE,
        db_column="visitteam",
        related_name="schedules_visitteam_set",
        default=0,
    )
    seriesid = models.AutoField(primary_key=True)
    homewins = models.IntegerField(default="0")
    visitwins = models.IntegerField(default="0")
    numgames = models.IntegerField(default="3")
    dateplayed = models.DateTimeField(blank=True, null=True)
    playmonth = models.IntegerField(choices=MONTH_CHOICES, blank=False, null=False)
    monthidx = models.IntegerField(choices=MONTHIDX_CHOICES, blank=False, null=False)

    class Meta:
        db_table = "schedules"
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        constraints = [
            models.UniqueConstraint(
                fields=["year", "hometeam", "visitteam", "playmonth", "monthidx"],
                name="unique_schedule",
            ),
        ]

    def __str__(self):
        return f"{self.visitteam} @ {self.hometeam} {self.playmonth} {self.monthidx}"


class SchedulesAdmin(admin.ModelAdmin):
    fields = [
        "year",
        "hometeam",
        "visitteam",
        "playmonth",
        "monthidx",
        "numgames",
        "homewins",
        "visitwins",
    ]
    list_filter = ("year",)
    list_display = (
        "seriesid",
        "year",
        "hometeam",
        "visitteam",
        "playmonth",
        "monthidx",
        "numgames",
    )
    search_fields = ["hometeam__nickname", "visitteam__nickname", "playmonth"]

    class Meta:
        db_table = "schedules"
