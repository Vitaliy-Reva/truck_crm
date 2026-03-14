import pandas
from ..models import NoPayedOrder, Order

class PaymentService:
    @staticmethod
    def payment_process(file):
        datas = pandas.read_excel(file, dtype=str)

        for _, rows in datas.iterrows():
            payment_id = rows.get("payment_id")
            
            if not payment_id:
                continue

            order = Order.objects.filter(pay_id=payment_id).exists()

            data = {
                "date": rows.get("Дата"),
                "pay_id": rows.get("payment_id"),
                "company": rows.get("Компанія"),
                "name": rows.get("ПІБ/Представник"),
                "ipn": rows.get("ІПН"),
                "edrpou": rows.get("ЄДРПОУ"),
                "total": rows.get("Сума")
            }
        
            if order:
                Order.objects.filter(pay_id=payment_id).update(payment_status='P')
            
            else:
                NoPayedOrder.objects.create(**data)