import pdfreader
from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.http import HttpResponse
from django.urls import reverse
from .forms import FileFieldForm
# from .forms import NameForm
from .handle_uploaded_file import HandleUploadedFile
from .models import Transaction, Transaction2, Statement
from django.db.models import Count, Sum
from django.db.models.functions import Round
import json

#check
months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
          "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

negative_sign = "-"


def get_negative_sign():  # Alternate between '-' and ''
    global negative_sign
    if negative_sign == "-":
        negative_sign = ""
    else:
        negative_sign = "-"
    return negative_sign





def index(request):

    if request.method == 'POST':

        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():

            files = form.cleaned_data['files']
            for f in files:
                uploaded_file = HandleUploadedFile(f)
                list_of_transactions: list = uploaded_file.get_transactions()
                # Uploaded file is a bank statement
                date_in_string = uploaded_file.date_of_the_statement  # Ex: "March 01, 2022"
                date_in_string = date_in_string.replace(",", "")  # remove comma


                if this_date_is_already_in_db(date_in_string):
                    continue

                # Write to Statement table
                pdf_statements = Statement(uploaded_statement_file=date_in_string)
                pdf_statements.save()

                # write each transaction to database: BankStatement
                for transaction in list_of_transactions:

                    # example of what transaction date returns: ['01/31', '01/30']
                    # One date tells when the purchase took place. The other date tells when the charge on the
                    # account was made.
                    mmdd = transaction.date[0].replace('/', '-')  # Ex: dd/dd -> dd-dd

                    mmddyyyy = get_only_month_and_year(date_in_string, just_year=True) + '-' + mmdd
                    current_object = Statement.objects.get(uploaded_statement_file=date_in_string)
                    transaction = Transaction(date=mmddyyyy,
                                                 description=transaction.store,
                                                 amount=transaction.amount,
                                                 statement_file=current_object)
                    transaction.save()


            return HttpResponseRedirect(reverse("page:index"))
        # return render(request, 'page/result.html', {'checked_boxes': selected_pdf_files})
    else:
        form = FileFieldForm()
    return render(request, 'page/index.html', {'form': form,
                                               'list_statements': Statement.objects.all()})


def result_page(request):
    list_of_boxes = request.POST.getlist('boxes')
    all_statements_of_selected_pdf_files = get_transactions_from_selected_statements(list_of_boxes)
    total = get_total_amount(all_statements_of_selected_pdf_files)
    if request.method == "POST":
        if "remove_statement" in request.POST:
            for selected_box in request.POST.getlist('boxes'):
                Statement.objects.filter(uploaded_statement_file=selected_box).delete()
            #  Don't jump to result page. Instead, stay at index page.
            return index(request)  # Not really a good solution. To be reviewed.

        id_set = request.POST.getlist("alist_of_ids")
        statement_str = Statement.objects.filter(id__in=id_set)  # Get objects for many IDs
        transactions = Transaction.objects.filter(statement_file__in=statement_str)

        if "add_to_table" in request.POST:
            selected_items: str = request.POST['add_to_table']
            selected_items: list = json.loads(selected_items)
            if selected_items[0].isdigit():
                selected_items = transactions.filter(id__in=selected_items)  # Filter items from main table
                for e in selected_items:
                    if not Transaction2.objects.filter(id=e.id):  # Do if the item selected is not present in second table.
                        transaction2 = Transaction2(date=e.date, description=e.description, amount=e.amount, id=e.id)
                        transaction2.save()
            else:
                for each in selected_items:
                    #  From one description we might get more than one ID.
                    #  Because some of the transactions have exactly the description.
                    ids_of_transactions = Transaction.objects.filter(description=each).values('id')
                    for id in ids_of_transactions:
                        matched_transaction = transactions.get(id=id['id'])
                        transaction2 = Transaction2(date=matched_transaction.date,
                                                    description=matched_transaction.description,
                                                    amount=matched_transaction.amount,
                                                    id=matched_transaction.id)
                        transaction2.save()

            transactions2 = Transaction2.objects.all()  # Which are the selected items from the main table
            # Exclude second table items from main table
            transactions = transactions.exclude(id__in=Transaction2.objects.all())
            return render(request, 'page/result.html', {'list_of_transactions': transactions,
                                                        'total': transactions.aggregate(Sum("amount"))["amount__sum"],
                                                        'list_of_selected_transactions': transactions2,
                                                        'total_selected_transactions':
                                                            transactions2.aggregate(Sum("amount"))["amount__sum"],
                                                        'selected_statements_ids': id_set})
        if "empty_table" in request.POST:
            Transaction2.objects.all().delete()
            return render(request, 'page/result.html', {'list_of_transactions': transactions,
                                                        'total': transactions.aggregate(Sum("amount"))["amount__sum"],
                                                        'selected_statements_ids': id_set
                                                        })
        action = request.POST.get("sort")
        if action == "amount" or action == "description":
            column = action  # change name
            column_with_sign = get_negative_sign() + column
            sorted_transactions = transactions.order_by(column_with_sign).\
                exclude(id__in=Transaction2.objects.all())
            sorted_transactions2 = Transaction2.objects.all().order_by(column_with_sign)
            return render(request, 'page/result.html', {'list_of_transactions': sorted_transactions,
                                                        'total': sorted_transactions.aggregate(Sum("amount"))["amount__sum"],
                                                        'list_of_selected_transactions': sorted_transactions2,
                                                        'total_selected_transactions':
                                                            sorted_transactions2.aggregate(Sum("amount"))["amount__sum"],
                                                        'selected_statements_ids': id_set})
        if "description_group" in request.POST:
            column_with_sign = get_negative_sign() + "dcount"
            grouped_transactions = (transactions
                                    .values('description')
                                    .annotate(dcount=Count('description'))
                                    .order_by(column_with_sign)
                                    .annotate(amount=Round(Sum('amount'), 2))
                                    ).exclude(id__in=Transaction2.objects.all())

            grouped_transactions2 = (Transaction2.objects.all()
                                     .values('description')
                                     .annotate(dcount=Count('description'))
                                     .order_by(column_with_sign)
                                     .annotate(amount=Round(Sum('amount'), 2))
                                     )
            return render(request, 'page/result.html', {'list_of_transactions': grouped_transactions,
                                                        'total': grouped_transactions.aggregate(Sum("amount"))["amount__sum"],
                                                        'list_of_selected_transactions': grouped_transactions2,
                        'total_selected_transactions': grouped_transactions2.aggregate(Sum("amount"))["amount__sum"],
                                                        'selected_statements_ids': id_set})
        if "keyword" in request.POST:
            return render(request, 'page/result.html', {'list_of_transactions': transactions,
                                                        'total': total,
                                                        'selected_statements_ids': id_set})

        return render(request, 'page/result.html', {'list_of_transactions': all_statements_of_selected_pdf_files,
                                                    'total': total,
                                                    'selected_statements_ids': get_list_of_ids(list_of_boxes),
                                                    'list_of_selected_transactions': Transaction2.objects.all(),
                                                    'total_selected_transactions':
                                                        Transaction2.objects.all().aggregate(Sum("amount"))["amount__sum"]
                                                    })

    else:
        return render(request, 'page/result.html', {'list_of_transactions': all_statements_of_selected_pdf_files,
                                                    'total': total,
                                                    'list_of_selected_transactions': Transaction2.objects.all(),
                                                    'total_selected_transactions':
                                                        Transaction2.objects.all().aggregate(Sum("amount"))["amount__sum"]
                                                    })




def get_list_of_ids(checked_box_list) -> list:
    res = []
    for each in checked_box_list:
        selected_pdf_model = Statement.objects.filter(uploaded_statement_file=each)  # Corresponding model
        selected_model_id = selected_pdf_model.get().id
        res.append(selected_model_id)
    return res



def get_transactions_from_selected_statements(checked_box_list):
    res = []
    for selected_box in checked_box_list:
        selected_pdf_model = Statement.objects.filter(uploaded_statement_file=selected_box)  # Corresponding model
        selected_model_id = selected_pdf_model.get().id

        for statement in Transaction.objects.filter(statement_file=selected_model_id):
            res.append(statement)
    return res


def get_only_month_and_year(date_in_string, just_year=False, just_month=False) -> str:  # "March 01, 2022" -> March 2022
    year = date_in_string[-4:]
    if just_year:
        return year
    month = date_in_string[:date_in_string.index(' ')]
    if just_month:
        return month
    return month + ' ' + year


def get_total_amount(transactions):
    total = 0
    for transaction in transactions:
        total += transaction.amount
    return total


def this_date_is_already_in_db(date_in_string):
    for each_statements_date in Statement.objects.all():
        if date_in_string == str(each_statements_date):
            return True
    return False
