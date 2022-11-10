
import unittest
from example.cart import ShoppingCart
from example.product import Product

class ShoppingCartTestCase(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        self.product = Product('Polo', 'S', 'Navy Blue')
    
    def test_cart_initially_empty(self):
        self.assertDictEqual({}, {}) 

    def test_add_and_remove_product(self):
        self.cart.add_product(self.product)
        self.cart.remove_product(self.product)
        # Check if the products attribute is empty
        # The assertDictEqual check if two dicts are equal
        self.assertDictEqual({}, self.cart.products) 
    
    def test_add_product(self):
        product = Product('Shoes', 'S', 'Blue')
        self.cart.add_product(product)
        self.assertDictEqual(self.cart.products, {'SHOES-S-BLUE': {'quantity': 1}}) 
    
    def test_add_two_of_a_product(self):
        product = Product('Shoes', 'S', 'Blue')
        self.cart.add_product(product, quantity=2)
        self.assertDictEqual(self.cart.products, {'SHOES-S-BLUE': {'quantity': 2}}) 

    def test_remove_too_many(self):
        cart = ShoppingCart()
        product = Product('shoes', 'S', 'blue')

        cart.add_product(product)
        cart.remove_product(product, quantity=1)

        self.assertDictEqual({}, cart.products)

        
unittest.main(argv=[''], verbosity=3, exit=False)



