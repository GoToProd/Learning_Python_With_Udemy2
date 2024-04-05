#import stripe
from http import HTTPStatus

from django.conf import settings
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt


from common.views import TitleMixin
from orders.forms import OrderForm
from products.models import Basket
from orders.models import Order


class SuccsessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/succsess.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/canceled.html'
    title = 'Store - Отмена заказа'
    
class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = ('-created')
    
    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Заказ №{self.object.id}'
        return context

#stripe.api_key = settings.STRIPE_SECRET_KEY

class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_success')
    title = 'Store - Оформление заказа'
    
    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        if self.object:  
            user=self.request.user
            # baskets = Basket.objects.filter(user=self.request.user)
            orders = Order.objects.filter(initiator=user)
            for order in orders:
                # order.status = Order.DELIVERED
                order.update_after_payment()
                # order.save()
            # for basket in baskets:
            #     basket.delete()
            #     basket.save()
        return HttpResponseRedirect(self.success_url, status=HTTPStatus.SEE_OTHER) 
        
        
        # session = ({
        #     success_url = '{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
        # })
        # = Stripe::Checkout::Session.create({
        #     line_items: [{
            #     price: '{{price-1................................}}',
            #     quantity: 1,
        #         }],
        #     metadata = {'order_id': self.object.id}
        #     mode: 'payment',
        #     success_url: '{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
        #     cancel_url: '{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        # })
        
        
        
        return HttpResponseRedirect(reverse_lazy('orders:order_success'), status=HTTPStatus.OK)
    
    
    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
    
# @csrf_exempt
# def stipe_webhook_view(request):
#     payload = request.body
#     print(payload)
#     return HttpResponse(status=200)

# def fulfill_order(self):
#     order_id = self.request.order.id
#     order = Order.objects.get(id=order_id)
#     order.update_after_payment()