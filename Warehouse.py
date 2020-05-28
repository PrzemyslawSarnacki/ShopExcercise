import csv
from decimal import Decimal

warehouse_file = open('Magazyn.csv')
warehouse_reader = csv.reader(warehouse_file)
warehouse_data = list(warehouse_reader)

order_file = open('Zamowienie.csv')
order_reader = csv.reader(order_file)
order_data = list(order_reader)

class Warehouse(object):
    # def __init__(self, product_id, quantity):
    #     self.product_id = product_id
    #     self.quantity = quantity
    
    def get_product(self):
        for product in warehouse_data:
            if product[0] == self.product_id:
                print("self.product_id")
                print(self.product_id)
                desired_product = product
                print(product)
                return desired_product

    def get_price(self):
        desired_product = self.get_product()
        print(desired_product)
        return (Decimal(desired_product[2]))
    
    def get_multiplied_price(self):
        desired_product = self.get_product()
        return (Decimal(desired_product[2]) * self.quantity)
    
    def get_name(self):
        desired_product = self.get_product()
        return (desired_product[1])
        
    def get_tax(self):
        desired_product = self.get_product()
        return (Decimal(desired_product[2]) * Decimal(desired_product[3]))
    
    def get_multiplied_tax(self):
        desired_product = self.get_product()
        return (Decimal(desired_product[2]) * self.quantity * Decimal(desired_product[3]))

    def get_netto(self):
        price = self.get_price()
        tax = self.get_tax()
        return price - tax

class Order(Warehouse):
    def __init__(self, quantity, product_id):
        self.quantity = quantity
        self.product_id = product_id

    def get_ids(self):
        id_list = []
        for product in order_data[1::]:
            if product[0].isnumeric(): 
                id_list.append(int(product[0]))
        return id_list

    def get_quantities(self):
        quantity_list = []
        for product in order_data[1::]:
            if product[1].isnumeric(): 
                quantity_list.append(int(product[1]))
        return quantity_list

    def get_prices(self):
        ids = self.get_ids()
        quantities = self.get_quantities()
        print(ids)
        # for product_id, quantity in zip(ids, quantities):
        #     print(f"product_id {product_id} quantity {quantity}")
        #     self.quantity = quantity
        #     self.product_id = product_id

        # print(self.product_id)
        return self.quantity * self.get_price()


product_id = '1'
quantity = 5

# shopping = Warehouse(product_id, quantity)
order = Order(quantity, product_id)
print(order.get_prices())
