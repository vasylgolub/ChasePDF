from django.db import models, migrations


class Statement(models.Model):
    uploaded_statement_file = models.CharField(max_length=50)  # It will contain just month and year

    objects = models.Manager()

    def __str__(self):
        return self.uploaded_statement_file


class Transaction(models.Model):
    date = models.DateField('Transaction Execution Date')
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    # The statement file that it belongs
    statement_file = models.ForeignKey(Statement, on_delete=models.CASCADE, null=True)

    # https://stackoverflow.com/questions/35543695/type-object-x-has-no-attribute-objects
    objects = models.Manager()

    def __str__(self):
        return self.description



# class Migration(migrations.Migration):
#     atomic = False # <<<< THIS LINE
#
#     dependencies = [
#         ('shop', '0004_product_imgfeat'),
#     ]
#
#     operations = [
#         migrations.RenameModel(
#             old_name='Category',
#             new_name='CategoryShop',
#         ),
#     ]

