# -*- coding: utf-8 -*-

import requests
import logging

from zope.interface import directlyProvides
from zope.interface import implements
from zope.component.interfaces import ObjectEvent
from restarter.policy.interfaces import IDisqusNotify, ISimpleAddButtons, ICompanyShareNotify
from restarter.policy import policyMessageFactory as _


TIMEOUT = 2
NOTIFY = 'http://localhost:9441'
NEW_USER_MAIL = """
Benvenuto in Facciamo il portale a sostegno delle aziende colpite dal terremoto.

Facciamo lo ritrovi all'indirizzo: http://www.facciamoadesso.it
Il regolamento è http://www.facciamoadesso.it/il-progetto/il-regolamento


Ti ricordiamo la filosofia di Facciamo.

Rivolto alle imprese coinvolte dal sisma
Solo le imprese con sede nei comuni colpiti dal terremoto possono offrire i loro prodotti o chiedere supporto gratuito su Facciamo.

Solo persone vere
Per poter operare su Facciamo (offrire, comprare, ecc.) è necessario registrarsi come persone, identificandosi in modo chiaro ed inserendo un numero di cellulare ed una email in quanto indispensabili per poter creare il contatto tra chi offre e chi compra.

Mettiamoci la faccia
Questo è un luogo di incontro di persone e quindi mettiamo la nostra foto per presentarci.

Offerte aggiornate
Chi offre prodotti è tenuto a mantenere aggiornata l’effettiva disponibilità degli stessi.

Si paga direttamente al venditore
Sul portale non avvengono transazioni economiche: i soggetti entrano in contatto ed organizzano pagamenti e consegna in assoluta autonomia.

La pazienza è solidarietà
La situazione nelle zone colpite è molto difficile: siamo on line …. ma trovare una connessione per chi è sul posto non è sempre immediato.

Smascheriamo i farabutti
Chiunque ritenga di aver individuato una persona o una impresa non esistente o un comportamento non corretto è tenuto a segnalarlo.

Facciamo_lo conoscere
Facciamo è una iniziativa di servizio alle imprese in difficoltà: segnaliamo l’esistenza del portale ed i prodotti offerti ai nostri conoscenti (email, social network, passaparola).


-------------------
Il team di Facciamo
"""

NEW_COMPANY = '''
%s,

ti confermiamo l'avvenuta registrazione dell'azienda %s (%s).

All'interno dell'area della tua azienda puoi:
 * abilitare l'amministrazione del tuo profilo aziendale anche altri utenti già presenti sul portale
 * creare lo scaffale dei prodotti
 * richiedere supporto gratuito ad altre aziende in base alle tue necessità

Non dimenticare che per coinvolgere i tuoi potenziali clienti è molto importante come racconti la tua azienda e i problemi che state vivendo in questa difficile fase. 
Accresci la tua reputazione invitando tuoi conoscenti e collaboratori a lasciare commenti sul tuo profilo aziendale e la visibilità dei prodotti che stai offrendo condividendoli nei loro social network.

Ti ricordiamo che con la registrazione ti sei impegnato a visitare ed aggiornare le pagine del tuo profilo almeno settimanalmente.

Il regolamento che hai accettato nella procedura di registrazione è visibile a questo indirizzo http://www.facciamoadesso.it/il-progetto/il-regolamento


-------------------
Il team di Facciamo
'''

NEW_EMPLOYEE = '''
%s,

%s ti ha associato all'azienda %s.
Da questo momento hai l'abilitazione per amministrare il profilo dell'azienda.

All'interno dell'area della tua azienda puoi anche:
  * creare lo scaffale dei prodotti
  * richiedere supporto gratuito ad altre aziende in base alle tue necessità

Non dimenticare che per coinvolgere i tuoi potenziali clienti è molto importante come racconti la tua azienda e i problemi che state vivendo in questa difficile fase. 
Accresci la tua reputazione invitando tuoi conoscenti e collaboratori a lasciare commenti sul tuo profilo aziendale e la visibilità dei prodotti che stai offrendo condividendoli nei loro social network.

Il regolamento è visibile a questo indirizzo http://www.facciamoadesso.it/il-progetto/il-regolamento


-------------------
Il team di Facciamo
'''


NEW_ORDER_MAIL = '''
Buon notizie,

%s ha prenotato %s %s su Facciamo.

Vedi la prenotazione %s.
Puoi contattare %s al suo cellulare (%s) o via email (%s) per accordarvi.
Per confermare la sua richiesta, ricordati di andare sulla prenotazione e premere su "accetta"


-------------------
Il team di Facciamo
'''


NEW_ORDER_SMS = '''%s ha effettuato una prenotazione su Facciamo. Vai alla tua email per contattarlo.'''


ORDER_ACCEPTED = '''
Complimenti,

%s ha confermato la tua prenotazione:

%s %s %s a %s euro - %s

Ti ricordiamo che il regolamento di Facciamo prevede che gli accordi di pagamento e di consegna siano stabiliti direttamente tra le parti.
I riferimenti del venditore sono disponibili a %s

Una volta completata la transazione, ti invitiamo a lasciare un commento sulla pagina dell'azienda.


-------------------
Il team di Facciamo
'''


ORDER_REJECTED = '''
%s,

purtroppo %s non ha potuto confermare la tua prenotazione %s

I riferimenti del venditore sono disponibili a %s

Guarda su http://www.facciamoadesso.it per scoprire altri prodotti interessanti.


-------------------
Il team di Facciamo
'''

NEW_COMMENT = 'You have received new comment to %s.'

logger = logging.getLogger('restarter.policy')



class DisqusNotify(ObjectEvent):
    implements(IDisqusNotify)

    def __init__(self, object, comment_id, comment_text):
        self.object = object
        self.comment_id = comment_id
        self.comment_text = comment_text


class CompanyShareNotify(ObjectEvent):
    implements(ICompanyShareNotify)

    def __init__(self, object, userid, add_user=True):
        self.object = object
        self.userid = userid
        self.add_user = add_user


def notify(endpoint, params):
    """Notify restarter.notify."""
    try:
        requests.post('%s/%s' % (NOTIFY, endpoint), params=params, timeout=TIMEOUT)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        logger.exception('Encountered an error while handling %s notification' % params)


def company_notify(company, params):
    #Who to notify
    notification_type = company.getNotification()
    phone = company.getCellphone()
    email = company.getEmail()

    if notification_type == 'phone':
        params.update({'phone': phone})
    elif notification_type == 'email':
        params.update({'email': email})
    elif notification_type == 'both':
        params.update({'email': email})
        params.update({'phone': phone})

    notify('notify', params)


def order_state_changed(order, event):
    owner = order.getOwner()
    email = owner.getProperty('email', '')
    company = order.getCompany()
    product = order.getProduct()
    unit = product.getUnit().decode('utf8','ignore')
    quantity = order.getQuantity()
    price = product.getPrice()
    total_price = float(quantity) * float(price)
    params = {}

    if event.action == 'accept':
        if email:
            params.update({'email_message': ORDER_ACCEPTED % (company.title_or_id().decode('utf8','ignore'),
                                                              quantity,
                                                              unit,
                                                              product.title_or_id().decode('utf8','ignore'),
                                                              total_price,
                                                              order.absolute_url(),
                                                              company.absolute_url(),
                                                              ),
                           'email': email})
        notify('notify', params)

    elif event.action == 'reject':
        if email:
            params.update({'email_message': ORDER_REJECTED % (owner.getProperty('fullname','Ciao!'),
                                                              company.title_or_id().decode('utf8','ignore'),
                                                              order.absolute_url(),
                                                              company.absolute_url(),
                                                              ),
                           'email': email})
        notify('notify', params)
    else:
        return


def order_added(order, event):
    """Every time a order is added - change title."""
    if order.Title():
        return
    product = order.getProduct()
    quantity = order.getQuantity().decode('utf8', 'ignore')
    title = product.title_or_id().decode('utf8','ignore')
    unit = order.getUnit().decode('utf8', 'ignore')
    order.setTitle(u'%s %s di %s' % (quantity, unit, title))
    order.reindexObject()
    company = order.getCompany()
    if not company:
        return

    owner = order.getOwner()
    params = {'email_message': NEW_ORDER_MAIL % (owner.getProperty('fullname','Utente'),
                                                 quantity,
                                                 title,
                                                 order.absolute_url(),
                                                 owner.getProperty('fullname','Utente'),
                                                 owner.getProperty('cellphone'),
                                                 owner.getProperty('email'),
                                                 ),
              'phone_message': NEW_ORDER_SMS % owner.getProperty('fullname','Utente')}
    company_notify(company, params)


def product_published(product, event):
    if event.action != 'publish':
        return
    member = product.portal_membership.getAuthenticatedMember()
    facebook_id = get_facebook_from_member(member)
    if facebook_id:
        params = {'facebook_id': facebook_id,
                  'product_url': product.absolute_url()}
        notify('notify/fb/sell', params)


def company_published(company, event):
    if event.action != 'publish':
        return
    member = company.portal_membership.getAuthenticatedMember()
    facebook_id = get_facebook_from_member(member)
    if facebook_id:
        params = {'facebook_id': facebook_id,
                  'company_url': company.absolute_url()}
        notify('notify/fb/newcompany', params)


def company_employee_modified(company, event):
    if event.add_user:
        owner = company.getOwner()
        member = company.portal_membership.getMemberById(event.userid)
        email = member.getProperty('email', '')
        if email:
            params = {'email_message': NEW_EMPLOYEE % (member.getProperty('fullname','Ciao!'),
                                                       owner.getProperty('fullname', 'UPV'),
                                                       company.title_or_id()),
                      'email': email}
            notify('notify', params)
    company.reindexObject(idxs=['company_employees'])


def company_added(company, event):
    """Every time a company is added - create substructure."""

    if 'prodotti' in company.objectIds():
        #stupid check - plone is calling it twice, why?
        return

    products = company[company.invokeFactory('Products','prodotti')]
    products.setTitle(u'Prodotti')
    directlyProvides(products, (ISimpleAddButtons,))
    products.reindexObject()

    if 'richieste' in company.objectIds():
        #stupid check - plone is calling it twice, why?
        return

    demands = company[company.invokeFactory('Demands','richieste')]
    demands.setTitle(u'Richieste')
    directlyProvides(products, (ISimpleAddButtons,))
    demands.reindexObject()

    if 'foto' in company.objectIds():
        #stupid check - plone is calling it twice, why?
        return

    media = company[company.invokeFactory('Folder','foto')]
    media.setTitle(u'Foto')
    media.setLayout('atct_album_view')
    company.portal_workflow.doActionFor(media, "publish",comment=_("Published on company creation"))
    media.setConstrainTypesMode(1)
    media.setLocallyAllowedTypes(['Image','File'])
    directlyProvides(media, (ISimpleAddButtons,))
    media.reindexObject()

    if 'docs' in company.objectIds():
        #stupid check - plone is calling it twice, why?
        return

    docs = company[company.invokeFactory('Folder','docs')]
    docs.setTitle(u'Documenti')
    docs.setLayout('folder_tabular_view')
    company.portal_workflow.doActionFor(docs, "publish",comment=_("Published on company creation"))
    docs.setConstrainTypesMode(1)
    docs.setLocallyAllowedTypes(['Document','CompanyStory','File'])
    directlyProvides(docs, (ISimpleAddButtons,))
    docs.reindexObject()

    owner = company.getOwner()

    params = {'email_message': NEW_COMPANY % (owner.getProperty('fullname', 'Ciao!'),
                                        company.title_or_id(),
                                        company.absolute_url()),}
    company_notify(company, params)
    company.portal_workflow.doActionFor(company, "create")

    company.manage_setLocalRoles(owner.getId(), ('Owner', 'Employee',))


def company_commented(company, event):
    """Event fired when company has been commented."""
    params = {'email_message': NEW_COMMENT % company.absolute_url(),}
    company_notify(company, params)


def product_added(product, event):
    """Event fired when product has been added."""
    if 'foto' in product.objectIds():
        #stupid check - plone is calling it twice, why?
        return
    media = product[product.invokeFactory('Folder','foto')]
    media.setTitle(u'Foto')
    media.setLayout('atct_album_view')
    directlyProvides(media, (ISimpleAddButtons,))
    media.setConstrainTypesMode(1)
    media.setLocallyAllowedTypes(['Image',])
    product.portal_workflow.doActionFor(media, "publish",comment=_("Published on product creation"))
    product.portal_workflow.doActionFor(product, "create")


def product_commented(product, event):
    """Event fired when product has been commented."""
    company = product.getCompany()
    params = {'email_message': NEW_COMMENT % product.absolute_url(),}
    company_notify(company, params)

    member = product.portal_membership.getAuthenticatedMember()
    email = member.getProperty('email', '')
    if email:
        params = {'email_message': NEW_COMMENT,
                  'email': email}
        notify('notify', params)


def offer_commented(product, event):
    """Event fired when offer has been commented."""
    member = product.getOwner()
    email = member.getProperty('email', '')
    if email:
        params = {'email_message': NEW_COMMENT,
                  'email': email}
        notify('notify', params)


def demand_commented(product, event):
    """Event fired when demand has been commented."""
    company = product.getCompany()
    params = {'email_message': NEW_COMMENT % product.absolute_url(),}
    company_notify(company, params)


def get_facebook_from_member(member):
    return member.getProperty('facebook_id', '')


def user_created(member, event):
    """Event fired when new user has been registered."""
    facebook_id = get_facebook_from_member(member)
    if facebook_id:
        params = {'facebook_id': facebook_id}
        notify('notify/fb/register', params)

    email = member.getProperty('email', '')
    if email:
        params = {'email_message': NEW_USER_MAIL,
                  'email': email}
        notify('notify', params)

#    phone = member.getProperty('cellphone', '')
#    if phone:
#        params = {'message': NEW_USER_SMS,
#                  'phone': phone}
#        notify('notify/sms', params)


