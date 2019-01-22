from django.db import models


class Test(models.Model):
    """

    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, db_index=True)
    test_name = models.CharField(max_length=100)
    slug = models.SlugField()
    published_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.test_name


class Question(models.Model):
    """
    
    """
    question = models.CharField(max_length=300)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    choice_1 = models.CharField(max_length=200)
    choice_2 = models.CharField(max_length=200)
    choice_3 = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.question)


class TestAttempt(models.Model):
    """
    model for attempting a test
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, db_index=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'test')

    def __str__(self):
        return self.marks
