from django.db import models

class Transport(models.Model):
    transport_model = models.CharField('Модель', max_length=40, null=True, blank=True)
    license_plate = models.CharField('Номера', max_length=10, null=True, blank=True)
    fuel_rate = models.IntegerField('Рівень палива', default=0, blank=True)
    vin = models.CharField('VIN-номер', max_length=17, null=True, blank=True, unique=True)
    mileage = models.SmallIntegerField('Пробіг', null=True, blank=True, default=0)
    photo = models.ImageField('Фото', upload_to = 'images/')
    status = models.CharField('Статус', max_length=20, choices=(('F', 'Вільний'), ('OW', 'В дорозі')), default='F')
    to = models.CharField('Технічне обслуговування', max_length=20, choices=(('NS', 'Потрібне ТО'), ('S', 'Обслужений'), ('OS', 'На обслуговувані'), ('R', 'В ремонті')), default='S')
    miles_to_inspect = models.SmallIntegerField('ТО раз в', null=True, blank=True, default=0)
    next_inspect = models.SmallIntegerField('Наступне ТО', null=True, blank=True, default=0)

    class Meta:
        ordering = ('transport_model',)
        verbose_name = "Транспорт"
        verbose_name_plural = "Транспорти"
    
    def __str__(self):
        return f"{self.transport_model} ({self.license_plate})"


class Driver(models.Model):
    first_name = models.CharField("Ім'я", max_length=50, null=True, blank=True)
    last_name = models.CharField('Прізвище', max_length=50, null=True, blank=True)
    phone = models.CharField('Номер телефону', max_length=13, null=True, blank=True, default='+380')
    photo = models.ImageField('Фото', upload_to='photos/')
    license = models.CharField('Посвідчення водія', max_length=100, null=True, blank=True)
    ipn = models.CharField('Ідентифікаційний код', max_length=10, null=True, blank=True, unique=True)
    experience = models.TextField('Досвід роботи. Про себе', max_length=500, null=True, blank=False)
    status = models.CharField('Статус', max_length=20, choices=(('F', 'Вільний'), ('OW', 'В дорозі'), ('W', 'Вихідний')), default='F')
    weekend_until = models.DateField('Вихідний до', null=True, blank=True)

    class Meta:
        ordering = ('last_name',)
        verbose_name = "Водій"
        verbose_name_plural = "Водії"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"


class Client(models.Model):
    client_type = models.CharField('Тип клієнта', max_length=10, choices=(('FIZ', 'Фізичне лице'), ('FOP', 'ФОП'), ('COMP', 'Компанія')))
    first_name = models.CharField("Ім'я", max_length=50, null=True, blank=True)
    last_name = models.CharField('Прізвище', max_length=50, null=True, blank=True)
    phone = models.CharField('Номер телефону', max_length=13, null=True, blank=True, default='+380')
    email = models.EmailField('Електронна пошта', max_length=127, null=True, blank=True)
    ipn = models.CharField('Ідентифікаційний код', max_length=10, null=True, blank=True, unique=True)
    company_name = models.CharField('Назва компанії', max_length=100, null=True, blank=True)
    edrpou = models.CharField('ЄДРПОУ', max_length=8, null=True, blank=True, unique=True)
    created = models.DateField('Дата створення', auto_now=True)

    class Meta:
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'

    def __str__(self):
        if self.client_type == 'FIZ':
            return f"{self.first_name} {self.last_name}"
        elif self.client_type == 'FOP':
            return f"ФОП {self.first_name} {self.last_name}"
        return f"{self.company_name}. Представник - {self.first_name} {self.last_name}"
    
    
class NoPayedOrder(models.Model):
    pay_id = models.IntegerField("Айді оплати", unique=True, primary_key=True)
    date = models.CharField('Дата', null=True, blank=True)
    company = models.CharField('Компанія', null=True, blank=True)
    name = models.CharField('ПІБ/Представник', null=True, blank=True)
    ipn = models.CharField('Ідентифікаційни код', max_length=10, null=True, blank=True)
    edrpou = models.CharField('ЄДРПОУ', max_length=8, null=True, blank=True)
    total = models.IntegerField('Сума', null=True, blank=True, default=0)

    class Meta:
        verbose_name = 'Не оплачене замовлення'
        verbose_name_plural = 'Не оплачені замовлення'

    def __str__(self):
        return f"({self.pay_id}) {self.name} ({self.company}) ({self.ipn}), ({self.edrpou})"
    

class Order(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    pay_id = models.IntegerField('Айді оплати', unique=True, null=True, blank=True)
    order_name = models.CharField('Назва замовлення', max_length=100, null=True, blank=True)
    price = models.SmallIntegerField('Ціна', null=True, blank=True, default=0)
    status = models.CharField('Статус доставки', null=True, blank=True, choices=(('W', 'Очікує'), ('D', 'Доставляється'), ('E', 'Доставлено')), default='W')
    address = models.CharField('Адреса доставки', max_length=300, null=True, blank=True)
    payment_status = models.CharField('Статус оплати', max_length=40, null=True, blank=True, choices=(('NP', 'Не оплачено'), ('P', 'Оплачено')), default='NP')
    date = models.DateField('Дата створення', auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ('client_id',)
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        
    def __str__(self):
        return f"{self.order_name} ({self.client_id})"


class Trip(models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    transport_id = models.ForeignKey(Transport, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    start_point = models.CharField('Старт', max_length=100, null=True, blank=True)
    end_point = models.CharField('Кінець', max_length=100, null=True, blank=True)
    status = models.CharField('Статус', max_length=20, choices=(('AC', 'Очікує підтвердження'), ('P', 'Виконується'), ('C', 'Виконано')), default='AC')
    distance = models.IntegerField('Відстань', null=True, blank=True, default=0)
    fuel_status = models.CharField('Статус пального', max_length=20, choices=(('O', 'Надвитрата'), ('N', 'Норма')), default='N')
    fuel_actual = models.IntegerField('Реальний об\'єм палива', null=True, blank=True, default=0)
    fuel_planned = models.IntegerField('Запланований об\'єм палива', null=True, blank=True, default=0)

    class Meta:
        verbose_name = "Поїздка"
        verbose_name_plural = "Поїздки"
    
    def __str__(self):
        return f"{self.start_point} - {self.end_point}"
    

class FuelLog(models.Model):
    transport_id = models.ForeignKey(Transport, on_delete=models.CASCADE)
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    liters = models.IntegerField('Літри', null=True, blank=True, default=0)
    price = models.DecimalField('Ціна', max_digits=15, decimal_places=2, null=True, blank=True, default=0)
    timestamp = models.DateTimeField('Дата заправки', auto_now_add=True)

    class Meta:
        verbose_name = "Паливо"
        verbose_name_plural = "Палива"
    
    def __str__(self):
        return f"{self.liters} ({self.price} грн)"


class Maintenance(models.Model):
    transport_id = models.ForeignKey(Transport, on_delete=models.CASCADE)
    type = models.CharField('Тип обслуговування', max_length=15, choices=(('S', 'ТО'), ('R', 'Ремонт'), ('E', 'Завершено')))
    cost = models.DecimalField('Ціна', max_digits=15, decimal_places=2, null=True, blank=True, default=0)
    date = models.DateField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = "Технічне обслуговування"
        verbose_name_plural = "Технічні обслуговування"
    
    def __str__(self):
        return f"{self.transport_id} ({self.type})"