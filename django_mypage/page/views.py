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
            only_month_and_year = get_only_month_and_year(date_in_string)

            # Write to ListOfStatementFiles table
            pdf_statements.uploaded_statement_file = only_month_and_year
            pdf_statements.save()

            # write each transaction to database: BankStatement
            for transaction in list_of_transactions:
                mmdd = transaction.date[0].replace('/', '-')  # Ex: dd/dd -> dd-dd

                mmddyyyy = get_only_month_and_year(date_in_string, just_year=True) + '-' + mmdd
                current_object = Statement.objects.get(uploaded_statement_file=only_month_and_year)
                bank_statement = Transaction(date=mmddyyyy,
                                             description=transaction.store,
                                             amount=transaction.amount,
                                             statement_file=current_object)
                bank_statement.save()


            return HttpResponseRedirect(reverse("page:index"))
        # return render(request, 'page/result.html', {'checked_boxes': selected_pdf_files})
    else:
        form = UploadFileForm()

    return render(request, 'page/index.html', {'form': form,
                                               'list_statements': Statement.objects.all()})
    # 'checked_boxes': request.POST.getlist('boxes')


def result_page(request, boxes=''):
    all_statements_of_selected_pdf_files = get_transactions_from_selected_statements(request.POST.getlist('boxes'))
    total = get_total_amount(all_statements_of_selected_pdf_files)

    if request.method == "POST":
        # return HttpResponseRedirect(reverse("page:result", {'list_of_transactions': all_transactions,
        #                                                     'total': total}))
        return render(request, 'page/result.html', {'list_of_transactions': all_statements_of_selected_pdf_files,
                                                    'total': total})

    else:
        return render(request, 'page/result.html', {'list_of_transactions': all_statements_of_selected_pdf_files,
                                                    'total': total})








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

