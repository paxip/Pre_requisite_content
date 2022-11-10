from collections import defaultdict
from example.product import Product



class ShoppingCart:
    def __init__(self):
        self.products = defaultdict(lambda: defaultdict(int))
        ## You should know what defauldict does by now. 

    def add_product(self, product, quantity=1):
        self.products[product.generate_sku()]['quantity'] += quantity

    def remove_product(self, product, quantity=1):
        sku = product.generate_sku()
        self.products[sku]['quantity'] -= quantity
        if self.products[sku]['quantity'] == 0:
            del self.products[sku]

if __name__ == "__main__":
    shoes = Product('Hugo Boss', 11, 'Black') 
    print(shoes.generate_sku())
    
