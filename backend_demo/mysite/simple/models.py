# import datetime
#
# from django.db import models
# from django.utils import timezone
#
#
# class Input(models.Model):
#     input_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#     def __str__(self):
#         return self.input_text
#
#     def was_published_recently(self):
#         return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


# class Output(models.Model):
#     input = models.ForeignKey(Input, on_delete=models.CASCADE)
#     output_text = models.CharField(max_length=200)
#     def __str__(self):
#         return self.output_text
