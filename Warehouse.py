import csv
from decimal import Decimal
from datetime import datetime

# wczytanie csv
with open('Magazyn.csv') as warehouse_file:
    warehouse_reader = csv.reader(warehouse_file)
    warehouse_data = list(warehouse_reader)
    
with open('Zamowienie.csv') as order_file:
    order_reader = csv.reader(order_file)
    order_data = list(order_reader)
    

class Client(object):
    def __init__(self, name, city, postcode, street, building_number, email, flat_number=""):
        self.name = name
        self.city = city
        self.postcode = postcode
        self.street = street
        self.building_number = building_number
        self.flat_number = flat_number
        self.email = email


class IndividualClient(Client):
    def __init__(self, first_name, surname, name, city, postcode, street, building_number, flat_number, email):
        super().__init__(name, city, postcode, street, building_number, flat_number, email)
        self.first_name = first_name
        self.surname = surname

    def get_individual_client(self):
        return f"{self.name}\n {self.first_name}\n, {self.surname}\n {self.city},\n {self.postcode},\n {self.street},\n {self.building_number},\n {self.flat_number},\n {self.email}\n"


class CompanyClient(Client):
    def __init__(self, economic_type, nip):
        super().__init__(name, city, postcode, street, building_number, flat_number, email)
        self.economic_type = economic_type 
        self.nip = nip 

    def get_company_client(self):
        return f"{self.name}\n {self.economic_type}\n, {self.nip}\n {self.city},\n {self.postcode}, \n {self.street},\n {self.building_number},\n {self.flat_number},\n {self.email}\n"


class Warehouse(object):
    # konstruktor dla "stanów" 
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity
    
    # pobieramy poszczególnego produktu z pliku Magazyn.csv
    def get_product(self):
        # przeszukujemy dane w postaci listy
        for product in warehouse_data:
            # jeśli natrafimy na produkt o danym id to zwracamy
            if product[0] == self.product_id:
                desired_product = product
                return desired_product
    
    # używając metody powyżej zwracamy cenę (jako Decimal - to prawie jak float)
    def get_price(self):
        desired_product = self.get_product()
        print(desired_product)
        # 2 pozycja to cena w csv
        return (Decimal(desired_product[2]))
    
    # to samo co wyżej tylko mnożymy przez ilość
    def get_multiplied_price(self):
        desired_product = self.get_product()
        return (Decimal(desired_product[2]) * self.quantity)
    
    # to samo co get_price tylko zwracamy nazwę (1 pozycja w pliku)
    def get_name(self):
        desired_product = self.get_product()
        return (desired_product[1])
        
    # to samo co get_price tylko zwracamy podatek (2 i 3 pozycja w pliku )
    def get_tax(self):
        desired_product = self.get_product()
        # czyli cena*stawkaVAT
        return (Decimal(desired_product[2]) * Decimal(desired_product[3]))
    
    def get_amount(self):
        desired_product = self.get_product()
        # czyli cena*stawkaVAT
        return (Decimal(desired_product[4]))
    
    # to samo co wyżej tylko wymnożone przez ilosc
    def get_multiplied_tax(self):
        desired_product = self.get_product()
        return (Decimal(desired_product[2]) * self.quantity * Decimal(desired_product[3]))

    # samo netto czyli brutto - podatek
    def get_netto(self):
        price = self.get_price()
        tax = self.get_tax()
        return price - tax

    def is_available(self, product_quantity):
        if self.get_amount() > product_quantity:
            return True
        else:
            return False

# klasa do zamówien
class Order(Warehouse):
    # zwracamy listę z id produktów z Zamowienie.csv
    def get_ids(self):
        id_list = []
        for product in order_data[1::]:
            if product[0].isnumeric(): 
                id_list.append((product[0]))
        return id_list


    # to samo co wyżej tylko dla ilości (2 kolumna w pliku - Ilosc)
    def get_quantities(self):
        quantity_list = []
        for product in order_data[1::]:
            if product[1].isnumeric():
                quantity_list.append(int(product[1]))
        return quantity_list
    
    # zwracamy listę z sumarycznymi cenami (ilosc * cena) używając tych 2 metod wyzej
    def get_prices(self):
        ids = self.get_ids()
        quantities = self.get_quantities()
        prices_list = []
        for product_id, quantity in zip(ids, quantities):
            print(f"product_id {product_id} quantity {quantity}")
            self.quantity = quantity
            self.product_id = product_id
            prices_list.append(self.quantity * self.get_price())
        return prices_list

    def get_total_price(self):
        ids = self.get_ids()
        quantities = self.get_quantities()
        total_price = Decimal()
        for product_id, quantity in zip(ids, quantities):
            self.quantity = quantity
            self.product_id = product_id
            total_price += self.quantity * self.get_price()
        return total_price
    
    def update_amount(self):
        return self.get_amount() - self.quantity

    def update_warehouse(self):
        warehouse_data
        desired_product = self.get_product()
        updated = []
        print(self.update_amount())
        for product in warehouse_data:
            if product == desired_product:
                product[4] = self.update_amount() 
            updated.append(product)
        return updated

    def update_csv(self):
        updated = self.update_warehouse()
        with open('Magazyn.csv', 'w', newline='') as csvfile:
            update_writer = csv.writer(csvfile, delimiter=',')
            update_writer.writerows(updated)
                    
                


# klasa do generowania faktur
class Invoice(Order):
    # tutaj sklejamy stringa, który będzie w fakturze
    def __init__(self, quantity, product_id, client_data):
        super().__init__(quantity, product_id)
        self.client_data = client_data

    def unique_number(self):
        date = datetime.now()
        hour_number = f"{date.day}/{date.hour}"
        return hour_number

    def get_date(self):
        date = datetime.now()
        day = f"{date.year}/{date.month}/{date.day}"
        hour = f"{date.hour}:{date.minute}"
        return (day, hour)

    def generate_invoice(self):
        prices_list = self.get_prices()
        # poczatkowy string z cenami taka pseudo tabela
        products_and_prices = "Nazwa | Cena |\n"
        # i tutaj dla wszystkich produktow dodajemy takiego f-stringa
        for i, price in enumerate(prices_list):
            products_and_prices += f"Produkt {i+1} | {str(price)} zl | \n"

        # wszystko do jednego ostatecznie wrzucamy 
        invoice_content = f"""
        {self.get_date()} {self.unique_number()}
        {self.client_data}\n
        {products_and_prices}
        Suma : {self.get_total_price()}
        """ 
        return invoice_content

    # zapisujemy stringa z metody wyzej do pliku 
    def write_to_file(self):
        invoice_content = self.generate_invoice()
        # otwieramy (jak nie ma tworzymy), zapisujemy stringa, zamykamy 
        f = open("invoice.txt", "w")
        f.write(invoice_content)
        f.close()


product_id = '2'
quantity = 5
# przez dziedziczenie po Warehouse musimy podać argumenty 
# mozna napisac init w Invoice by nie podawać lub coś innego wycudowac
# def __init__(self):
    # pass
# individual_client = IndividualClient("Imie", "Nazwisko", "Nazwa" ,"Miasto", "999-99", "ul.Ulica", 33, 3, "mail@mail.com")
# invoice = Invoice(quantity, product_id, individual_client.get_individual_client())
# invoice.write_to_file()
warehouse = Order(product_id, quantity)
warehouse.update_csv()