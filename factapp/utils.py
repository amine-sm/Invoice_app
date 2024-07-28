from .models import *

def get_invoice(pk):
    """ get invoice fonction """

    obj = Facture.objects.get(pk=pk)

    articles = obj.article_set.all()

    context = {
        'obj': obj,
        'articles': articles,
        'facture':obj
    }

    return context