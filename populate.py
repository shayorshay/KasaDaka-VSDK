import os
import sys
import re
import django
import datetime

def post_sms(caller_id, message_body, message_date):
        textmessage = TextMessage()
	textmessage.caller_id = caller_id
	textmessage.sms_body = message_body
	textmessage.sms_date = message_date
	textmessage.save()

def parse_outgoing_transaction(sms, message_date):
        transaction = Transaction()
        id_pattern = 'Transaction ID: ([0-9]+)'
        id = re.findall(id_pattern, sms)
        if len(id) == 1:
            id = id[0]
            transaction.id = id

        amount_pattern = 'for GHS([0-9]+.[0-9]{2})'
        amount = re.findall(amount_pattern, sms)
        if len(amount) == 1:
            amount = amount[0]
            transaction.amount = amount

        transaction.date = message_date.strftime("%y-%m-%d %H:%M:%S")

        reference_pattern = 'Reference: ([A-Za-z]+\s*[A-Za-z|\s]*)\.'
        reference = re.findall(reference_pattern, sms)
        if len(reference) == 1:
            reference = reference[0]
            transaction.reference = reference

        customer_pattern = 'to ([A-Za-z]+\s*[A-Za-z|\s]*)\.'
        customer = re.findall(customer_pattern, sms)
        customer = customer[0]
        transaction.customer_name = customer

        transaction.transaction_type = 'OUT'

        transaction.save()

def parse_incoming_transaction(sms):
        transaction = Transaction()
        print(sms)
        id_pattern = '([0-9]+) Confirmed'
        id = re.findall(id_pattern, sms)
        if len(id) == 1:
            id = id[0]
            transaction.id = id
            
        date_pattern = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        date = re.findall(date_pattern, sms)
        if len(date) == 1:
            date_of_deposit = ''.join(date[0])

        time_pattern = '[0-9]{2}:[0-9]{2}:[0-9]{2}'
        time = re.findall(time_pattern, sms)
        if len(time) == 1:
            time_of_deposit = ''.join(time[0])
            transaction.date = date_of_deposit + ' ' + time_of_deposit
            
        amount_pattern = 'GHS([0-9]+.[0-9]{2})'
        amount = re.findall(amount_pattern, sms)
        if len(amount) == 1:
            amount = amount[0]
            transaction.amount = amount
            
        reference_pattern = 'Reference: ([A-Za-z]+\s*[A-Za-z|\s]*)\.'
        reference = re.findall(reference_pattern, sms)
        if len(reference) == 1:
            reference = reference[0]
            transaction.reference = reference
            
        customer_pattern = 'from ([A-Za-z]+\s*[A-Za-z|\s]*)\.'
        customer = re.findall(customer_pattern, sms)
        customer = customer[0]
        transaction.customer_name = customer
        
        transaction.save() 



def post_transaction(sms, message_date):
        print(sms)
        out_pattern = 'Payment made'
        out_trans = re.findall(out_pattern, sms)
        if len(out_trans) == 1:
            parse_outgoing_transaction(sms, message_date)

        in_pattern = 'Confirmed'
        in_trans = re.findall(in_pattern, sms)
        if len(in_trans) == 1:
            parse_incoming_transaction(sms)
        

	
def get_data():
        caller_id = sys.argv[1]
        message_body = ' '.join(sys.argv[2:])
        message_date = datetime.datetime.now()
        post_sms(caller_id, message_body, message_date)
        #check if SMS is a transaction
        post_transaction(message_body, message_date)
       
if __name__ == '__main__':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vsdk.settings")
        django.setup()
        from vsdk.service_development.models import TextMessage
        from vsdk.service_development.models import Transaction
        get_data()
