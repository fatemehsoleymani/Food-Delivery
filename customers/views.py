from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from .models import MenuItem, OrderModel, Category
from django.core.mail import send_mail


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customers/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customers/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into content
        context = {
            'appetizers': appetizers,
            'desserts': desserts,
            'drinks': drinks
        }

    # render the template
        return render(request, 'customers/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        state = request.POST.get('state')
        city = request.POST.get('city')
        street = request.POST.get('street')
        zip_code = request.POST.get('zip_code')
        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(price=price,
                                          name=name,
                                          email=email,
                                          state=state,
                                          city=city,
                                          street=street,
                                          zip_code=zip_code,
                                          )
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to the user

        body = ('Thank you for your order! Yor food will be deliver soon! \n'
                f'Your total :{price}\n'
        )
        send_mail(
            'Thank You For Your Order',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk,  *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,

        }

        return render(request, 'customers/order_cofirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        print(request.body)


class OrderPayConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        return render(request, 'customers/order_pay_confirmation.html')


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }
        return render(request, 'customers/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }
        return render(request, 'customers/menu.html', context)
