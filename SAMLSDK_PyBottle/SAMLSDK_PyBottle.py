#Main Application

import bottle
import os
import sys
import SAML_Interface
import uuid

from bottle import Bottle, route, view, run, redirect, request, response, ServerAdapter, jinja2_view
from datetime import datetime

if '--debug' in sys.argv[1:] or 'SERVER_DEBUG' in os.environ:
    # Debug mode will enable more verbose output in the console window.
    # It must be set at the beginning of the script.
    bottle.debug(True)

def wsgi_app():
    #Returns the application to make available through wfastcgi. This is used when the site is published to Microsoft Azure.
    return bottle.default_app()

if __name__ == '__main__':
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    PORT = 6321

    @bottle.route('/static/<filepath:path>')
    def server_static(filepath):
        #Handler for static files, used with the development server. When running under a production server such as IIS or Apache, the server should be configured to serve the static files.
        return bottle.static_file(filepath, root=STATIC_ROOT)

#Http Routing

    #Defult
    @route('/')
    @route('/default')
    @view('default')
    def default():        
        strAcsUrl = 'http://localhost:6321/acs'
        strIssuer = 'https://cloud.centrify.com/SAML/GenericSAML'
        strIdentityProviderSigninURL = 'https://aaa3021.my-kibble.centrify.com/applogin/appKey/583e4d88-a193-4ea8-b306-e053b7fe2b7b/customerId/AAA3021'  
                  
        bottle.redirect('{uIDPUrl}?{bParams}'.format(uIDPUrl = strIdentityProviderSigninURL, bParams = SAML_Interface.SAML_Request.GetSAMLRequest(strAcsUrl, strIssuer)))       

    #ACS
    @route('/acs', method=['GET','POST'])
    @view('acs')
    def acs():
        samlResponse = request.forms['SAMLResponse']
        strAcsUrl = 'http://localhost:6321/acs'
        return dict(
            title='ACS',
            message=SAML_Interface.SAML_Response.ParseSAMLResponse(strAcsUrl,samlResponse),
            year=datetime.now().year
        )

    # Starts a local test server.
    bottle.run(server='wsgiref', host=HOST, port=PORT)
