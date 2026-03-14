from ..models import Order, Client, NoPayedOrder

class OrderService:
    @staticmethod
    def create_order(data: dict, client: Client):
        data['client_id'] = client

        order = Order.objects.create(**data)

        unpaid_payment = NoPayedOrder.objects.filter(pay_id=order.pay_id).first()

        if unpaid_payment:
            order.payment_status = 'P'
            order.save(update_fields=["payment_status"])
            unpaid_payment.delete()

        client.save()
        return order
    
    def update_order(data: dict, order: Order, client: Client):
        data['client_id'] = client

        order.save()
        client.save()

        return order