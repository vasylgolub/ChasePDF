from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.http import HttpResponse
from django.urls import reverse
from .forms import UploadFileForm
# from .forms import NameForm
from .handle_uploaded_file import HandleUploadedFile
from .models import Transaction, Statement


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
    pdf_statements = Statement()


    if request.method == 'POST':


        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            file = form.cleaned_data['file']

            uploaded_file = HandleUploadedFile(file)
            list_of_transactions: list = uploaded_file.get_transactions()

            # Uploaded file is a bank statement
            date_in_string = uploaded_file.date_of_the_statement  # Ex: "March 01, 2022"
            date_in_string = date_in_string.replace(",", "")  # remove comma

            # Write to Statement table
            pdf_statements.uploaded_statement_file = date_in_string
            pdf_statements.save()

            # write each transaction to database: BankStatement
            for transaction in list_of_transactions:
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
        form = UploadFileForm()
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



        if "amount_sort" in request.POST or "description_sort" in request.POST:
            id_set = request.POST.getlist("alist_of_ids")
            statement_ids = Statement.objects.filter(id__in=id_set)  # Get objects for many IDs
            transactions = Transaction.objects.filter(statement_file__in=statement_ids)

            column = "amount" if "amount_sort" in request.POST else "description"
            transactions = transactions.order_by(get_negative_sign()+column)

            total = get_total_amount(transactions)
            return render(request, 'page/result.html', {'list_of_transactions': transactions,
                                                        'total': total,
                                                        'selected_statements_ids': id_set})


        return render(request, 'page/result.html', {'list_of_transactions': all_statements_of_selected_pdf_files,
                                                    'total': total,
                                                    'selected_statements_ids': get_list_of_ids(list_of_boxes)})

    else:
        return render(request, 'page/result.html', {'list_of_transactions': all_statements_of_selected_pdf_files,
                                                    'total': total})





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

