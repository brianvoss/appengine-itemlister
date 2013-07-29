import cgi
import os
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

_DEBUG = True

class BaseRequestHandler(webapp2.RequestHandler):
  """Base request handler extends webapp.Request handler

     It defines the generate method, which renders a Django template
     in response to a web request
  """

  def generate(self, template_name, template_values={}):
    """Generate takes renders and HTML template along with values
       passed to that template

       Args:
         template_name: A string that represents the name of the HTML template
         template_values: A dictionary that associates objects with a string
           assigned to that object to call in the HTML template.  The defualt
           is an empty dictionary.
    """
    # We check if there is a current user and generate a login or logout URL
    user = users.get_current_user()

    if user:
      log_in_out_url = users.create_logout_url('/')
      log_in_out_text = 'Logout'
    else:
      log_in_out_url = users.create_login_url(self.request.path)
      log_in_out_text = 'Login'

    # We'll display the user name if available and the URL on all pages
    values = {'user': user, 'log_in_out_url': log_in_out_url, 'log_in_out_text':log_in_out_text}
    values.update(template_values)

    # Construct the path to the template
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, 'templates', template_name)

    # Respond to the request by rendering the template
    return template.render(path, values, debug=_DEBUG)
    
class MainRequestHandler(BaseRequestHandler):
  """ Main request handler """
  def get(self):
    self.response.out.write(self.generate('index.html', template_values));
    

application = webapp2.WSGIApplication(
                                      [('/', MainRequestHandler)],
                                      debug=_DEBUG)
  (