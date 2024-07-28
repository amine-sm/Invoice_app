from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from .decorators import *
from django.http import HttpResponse
import pdfkit
import datetime
from django.core.paginator import (Paginator,EmptyPage,PageNotAnInteger)
from django.utils.translation import gettext as _
from .utils  import get_invoice
class HomeView(LoginRequiredMixin,View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs): 
        factures = Facture.objects.select_related('customer', 'saved_by').order_by('-facture_date')
          
        default_page = 1
        page = request.GET.get('page', default_page)
        items_per_page = 8
        paginator = Paginator(factures, items_per_page)
        
        try:
            factures_page = paginator.page(page)
        except PageNotAnInteger:
            factures_page = paginator.page(default_page)
        except EmptyPage:
            factures_page = paginator.page(paginator.num_pages)
            
        context = {
            'factures': factures_page
        }
   
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Modifier 
        if request.POST.get('id_modified'):
            paid = request.POST.get('modified')
            try:
                obj = Facture.objects.get(id=request.POST.get('id_modified'))

                if paid == 'True':
                    obj.paid = True
                else:
                    obj.paid = False
                obj.save()
                messages.success(request, _("Change has been made successfully"))
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

        if request.POST.get('id_supprimer'):
                 try:
                       obj = Facture.objects.get(pk=request.POST.get('id_supprimer'))
                       obj.delete()
                       messages.success(request, _("the deletion was successful"))
                 except Exception as e:
                        messages.error(request, f"An error occurred: {e}")
       
        return redirect('home')  # Redirect to the GET view after processing the POST request

class AddCustomer(LoginRequiredMixin,View):
    template_name = "add_customer.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
      
    def post(self, request, *args, **kwargs): 
        data ={
          'name':request.POST.get('name'),
            'email':request.POST.get('email'),
              'phone':request.POST.get('phone'),
                'address':request.POST.get('address'),
                  'sex':request.POST.get('sex'),
                    'age':request.POST.get('age'),
                      'city':request.POST.get('city'),
                            'zip_code':request.POST.get('zip'),
                              'saved_by':request.user,
       }
        try :
            created=Customer.objects.create(**data)
            if  created :
                        messages.success(request,"Customer registed succefully")
            else :
                 messages.error(request,"Sorry ,please try later")           
        
        except Exception as e:
                   messages.error(request, f"Sorry, our system is detecting the following issues: {e}")
        return render(request, self.template_name)  # You can add context if needed

class AddInvoiceView(LoginRequiredMixin,View):
    template_name = "add_invoice.html"

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.select_related('saved_by').all()
        articles=Article.objects.all()
        context = {
            'customers': customers,
            'articles':articles
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            customer_id = request.POST.get('customer')
            invoice_type = request.POST.get('invoice_type')
            comment = request.POST.get('comment')
            items = []

            article_ids = request.POST.getlist('article')
            quantities = request.POST.getlist('qty')
            unit_prices = request.POST.getlist('unit')
            total_amounts = request.POST.getlist('total-a')

            total = request.POST.get('total')

            invoice_object = {
                'customer_id': customer_id,
                'saved_by': request.user,
                'total': total,
                'facture_type': invoice_type, 
                'commenter': comment
            }

            invoice = Facture.objects.create(**invoice_object)

            for article_id, qty, unit_price, total_amount in zip(article_ids, quantities, unit_prices, total_amounts):
                article = Article(
                    facture=invoice,
                    name=article_id,  # You should have a proper way to fetch the name of the article
                    quantite=qty,
                    prix_unite=unit_price,
                    total=total_amount
                )
                items.append(article)

            Article.objects.bulk_create(items)

            messages.success(request, "Invoice created successfully.")
        
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return render(request, self.template_name)
class InvoiceView(LoginRequiredMixin,View):
         template_name = "invoice.html"
         def get(self, request, *args, **kwargs):
               pk=kwargs.get('pk')
               obj=Facture.objects.get(pk=pk)
               articles=obj.article_set.all()

               context = {
              'obj':obj,
              'articles': articles
                  }
               return render(request, self.template_name, context)
        
class InvoiceView(View):
     template_name='invoice.html'
     def get(self, request, *args, **kwargs):
               pk=kwargs.get('pk')
               context=get_invoice(pk)
               return render(request, self.template_name, context)

@superuser_required
def get_invoice_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    pk = kwargs.get('pk')

    context = get_invoice(pk)

    context['date'] = datetime.datetime.today()

    # get html file
    template = get_template('invoice-pdf.html')

    # render html with context variables

    html = template.render(context)

    # options of pdf format 

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }

    # generate pdf 

    pdf = pdfkit.from_string(html, False, options)

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = "attachement"

    return response