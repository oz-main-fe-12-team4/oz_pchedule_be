from django.db import models


class Like(models.Model):
    like_id = models.IntegerField(primary_key=True, auto_created=True)
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE)
    post_id = models.ForeignKey("schedule.Post", on_delete=models.CASCADE)

    class Meta:
        db_table = "like"

    def __str__(self):
        return f"like ID = {self.like_id}"


class Favorite(models.Model):
    favorite_id = models.IntegerField(primary_key=True, auto_created=True)
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE)
    post_id = models.ForeignKey("schedule.Post", on_delete=models.CASCADE)

    class Meta:
        db_table = "favorite"

    def __str__(self):
        return f"favorite ID = {self.favorite_id}"


class Report(models.Model):
    report_id = models.IntegerField(primary_key=True, auto_created=True)
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE)
    post_id = models.ForeignKey("schedule.Post", on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = "report"

    def __str__(self):
        return f"report ID = {self.report_id}"
