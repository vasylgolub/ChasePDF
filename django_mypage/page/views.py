from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.http import HttpResponse
from django.urls import reverse
from .forms import UploadFileForm
# from .forms import NameForm
from .handle_uploaded_file import HandleUploadedFile
from .models import BankStatement, ListOfStatementFiles


# To do
# read this post to address the problem of getting duplicate uploads of files when refreshing the page
# https://stackoverflow.com/questions/65925084/uploading-duplicated-files-with-django-when-reloading-page
months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
          "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}


def index(request):
    statements = ListOfStatementFiles()
    list_of_statements = []
    if request.method == 'POST':
        checked_boxes_list = request.POST.getlist('boxes')
        for selected_box in checked_boxes_list:
            for i in BankStatement.objects.filter(date__month=months.get(selected_box)).values():
                list_of_statements.append(i)
                print(i)


        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            file = form.cleaned_data['file']
            uploaded_file = HandleUploadedFile(file)
            list_of_transactions: list = uploaded_file.get_transactions()

            date_in_string = uploaded_file.date_of_the_statement
            year = date_in_string[-4:]
            month = date_in_string[:date_in_string.index(' ')]
            month_and_year = month + ' ' + year

            statements.uploaded_statement_file = month_and_year
            statements.save()

            # insert transactions into database table
            for transaction in list_of_transactions:
                mmdd = transaction.date[0].replace('/', '-')
                mmddyyyy = year + '-' + mmdd
                bank_statement = BankStatement(date=mmddyyyy,
                                               description=transaction.store,
                                               amount=transaction.amount)
                bank_statement.save()


            return HttpResponseRedirect(reverse("page:index"))
        return render(request, 'page/result.html', {'list_of_transactions': list_of_statements,
                                                    'total': get_total_amount(list_of_statements)})
    else:
        form = UploadFileForm()


    return render(request, 'page/index.html', {'form': form,
                                               'list_statements': ListOfStatementFiles.objects.all()})



def result_page(request):
    all_transactions = BankStatement.objects.all()
    total = 0
    for transaction in all_transactions:
        total += transaction.amount

    if request.method == "POST":
        # text = request.POST['just_a_text']
        # return render(request, 'page/result.html', {'text': text})
        # assert False

        return HttpResponseRedirect(reverse("page:result", {'list_of_transactions': all_transactions, 'total': total}))
    else:
        return render(request, 'page/result.html', {'list_of_transactions': all_transactions, 'total': total})


def get_total_amount(transactions):
    total = 0
    for transaction in transactions:
        total += transaction.get('amount')
    return total
