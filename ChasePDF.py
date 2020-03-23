from PyPDF2 import PdfFileReader
import re
import os
###################################

class transaction:
    def __init__(self, whole_string, date, store, price):
        self.whole_string = whole_string
        self.date = date
        self.store = store
        self.price = price

def clean(unclean):
    return unclean[re.search(r'\d', str(unclean)).start():].replace(',',"")

# a reminder: when comparing the total price result with the total purchases written on the chase pdf, the chase pdf
# includes the cash back, which the ChasePDF class does not include.

class ChasePDF:# cccccccccccccccccccc start class ccccccccccccccccccccccccccc

    def __init__(self, path):
        self.purchases = []
        self.returns = []
        self.deposit = []
        p = open(path, 'rb')
        pdf = PdfFileReader(p)
        tot_pages = pdf.getNumPages()

        for page in range(tot_pages):
            current_page = pdf.getPage(page)
            text = current_page.extractText()  # we extract text from current page in the pdf
            # print(text)

            # some text will have "Purchase...dd\dd" which we don't need. Those text occur when I attempted
            # to buy something with insufficient fund. In that case that text we don't need. That's why
            # I made re.compile with word "Purchas" and not "Purchase", we need to make sure that there is
            # space after the word Purchase and then the dd/dd
            pattern = re.compile(r'Purchas(.+?)(\s\d{2}/\d{2})(.+?)6427((.+?)\.\d\d)')#(?=\s) is until space but excluding it
            matches = pattern.finditer(text)    # Get all the strings that matches the pattern.
                                                # It will be more than one, probably


            #**************************************** Deposit ********************************************************
            pattern2Deposit = re.compile(r'Deposit(\s+?)(\d{2}/\d{2})(.+?)6427(.+?)(\d{2}/\d{2})')
            pattern2Deposit2 = re.compile(r'Deposit(\s+?)(\d\d\d(.+?))(\d\d/\d\d)')  #Deposit        210091141,000.0001/14ATM
                                                                                     #Deposit  1838156494930.0003 / 20
                                                                                     #Deposit        21189791$616.0003/04ATM
            matches2 = pattern2Deposit.finditer(text)
            for m in matches2:
                final_num = m.group(4).replace(",","")
                if final_num.find("$") >= 0:
                    final_num = final_num[1:]
                t = transaction(m.group(0), m.group(4), "null", final_num)
                self.deposit.append(t)

            matches2 = pattern2Deposit2.finditer(text)
            for m in matches2: # group 4 is date, 0 is whole
                final_num = 0 # equals 0 for now
                num = m.group(2)
                dollar_sign = str(num).find("$")
                comma = str(num).find(",")
                if dollar_sign >= 0:
                    final_num = num[dollar_sign+1:].replace(",","")
                elif comma >= 0:
                    final_num = num[comma-1:].replace(",","")
                elif len(num) <= 6:
                    final_num = num
                else:
                    final_num = num[-6:]
                t = transaction(m.group(0), m.group(4), "null", final_num.replace(",", ""))
                self.deposit.append(t)
            # *************************************** end Deposit ****************************************************


            # ``````````````````````````````````````inner for loop`````````````````````````````````````````````````````

            for match in matches:# all the matches contain "Purchase Return" and just "Purchase .../ with ..." and etc.
                                    # What we need to do is to separate the returns from purchases.
                                    #  Because Returns contain
                                    # "Purchase" string also

                 # ----------------------------------------------------------
                unclean = match.group(4)  # unclean price that contains words and numbers
                clean = unclean[re.search(r'\d', str(unclean)).start():].replace(',',"")  # we clean the letters
                                                                                        # so we have only the price
                # -----------------------------------------------------------
                if match.group(0).find("Return") >= 0:
                    t = transaction(match.group(0), match.group(2), match.group(3), clean)
                    self.returns.append(t)
                else:
                    t = transaction(match.group(0), match.group(2), match.group(3), clean)
                    self.purchases.append(t)
            # `````````````````````````````````````end inner for loop`````````````````````````````````````````````````
# cccccccccccccccccccccccccc end class ccccccccccccccccccccccccccccccccccc



# print(t[re.search(r'\d',t).start():].replace(',',""))#from index of first found digit in a string to the end



months = ["january","fabruary","march","april","may","june","july","august","september","october","november","december"]


