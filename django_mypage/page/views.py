from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.http import HttpResponse
from django.urls import reverse
from .forms import UploadFileForm
# from .forms import NameForm
from .handle_uploaded_file import HandleUploadedFile
from .models import BankStatement, ListOfStatementFiles


months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
          "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}


def index(request):
    pdf_statements = ListOfStatementFiles()
    selected_pdf_files = []
    if request.method == 'POST':
        checked_boxes_list = request.POST.getlist('boxes')
        for selected_box in checked_boxes_list:
            for i in BankStatement.objects.filter(date__month=months.get(selected_box)).values():
                selected_pdf_files.append(i)

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            file = form.cleaned_data['file']
            uploaded_file = HandleUploadedFile(file)
            list_of_transactions: list = uploaded_file.get_transactions()

            date_in_string = uploaded_file.date_of_the_statement  # Ex: "March 01, 2022"
            only_month_and_year = get_only_month_and_year(date_in_string)
            pdf_statements.uploaded_statement_file = only_month_and_year
            pdf_statements.save()

            # write each transaction to database: BankStatement
            for transaction in list_of_transactions:
                mmdd = transaction.date[0].replace('/', '-')  # Ex: dd/dd -> dd-dd

                mmddyyyy = get_only_month_and_year(date_in_string, just_year=True) + '-' + mmdd
                current_object =  ListOfStatementFiles.objects.get(uploaded_statement_file=only_month_and_year)
                bank_statement = BankStatement(date=mmddyyyy,
                                               description=transaction.store,
                                               amount=transaction.amount)
                bank_statement.save()


            return HttpResponseRedirect(reverse("page:index"))
        return render(request, 'page/result.html', {'list_of_transactions': selected_pdf_files,
                                                    'total': get_total_amount(selected_pdf_files)})
    else:
        form = UploadFileForm()


    return render(request, 'page/index.html', {'form': form,
                                               'list_statements': ListOfStatementFiles.objects.all()})



def result_page(request):
    all_transactions = BankStatement.objects.values()
    total = get_total_amount(all_transactions)

    if request.method == "POST":
        return HttpResponseRedirect(reverse("page:result", {'list_of_transactions': all_transactions, 'total': total}))
    else:
        return render(request, 'page/result.html', {'list_of_transactions': all_transactions, 'total': total})





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
        total += transaction.get('amount')
    return total
