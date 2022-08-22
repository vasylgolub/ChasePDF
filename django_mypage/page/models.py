from django.db import models


class BankStatement(models.Model):
    date = models.DateField('Transaction Execution Date')
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    # https://stackoverflow.com/questions/35543695/type-object-x-has-no-attribute-objects
    objects = models.Manager()

    def __str__(self):
        return self.description


class ListOfStatementFiles(models.Model):
    uploaded_statement_file = models.CharField(max_length=50)

    objects = models.Manager()

    def __str__(self):
        return self.uploaded_statement_file


