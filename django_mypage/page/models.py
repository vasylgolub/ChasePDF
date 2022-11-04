from django.db import models


class ListOfStatementFiles(models.Model):
    uploaded_statement_file = models.CharField(max_length=50)  # It will contain just the month and year

    objects = models.Manager()

    def __str__(self):
        return self.uploaded_statement_file


class BankStatement(models.Model):
    date = models.DateField('Transaction Execution Date')
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    # The statement file that it belongs
    statement_file = models.ForeignKey(ListOfStatementFiles, on_delete=models.CASCADE, null=True)

    # https://stackoverflow.com/questions/35543695/type-object-x-has-no-attribute-objects
    objects = models.Manager()

    def __str__(self):
        return self.description





