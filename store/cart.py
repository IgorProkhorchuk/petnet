from django.conf import settings
from .models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    
    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
        
        for item in self.cart.values():
            item['total price'] = int(item['product'].price * item['quantity']) / 100

            yield item


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True


