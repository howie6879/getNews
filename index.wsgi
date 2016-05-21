import sae
sae.add_vendor_dir('vendor')
import tornado.wsgi
from application import application


application = sae.create_wsgi_app(application)