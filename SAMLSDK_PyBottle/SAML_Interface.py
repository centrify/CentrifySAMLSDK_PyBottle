import bottle
import zlib
import base64
import uuid
import urllib

from signxml import XMLVerifier
from base64 import b64decode

from datetime import datetime

from lxml import etree
from lxml.builder import ElementMaker

class SAML_Request:
    def GetSAMLRequest(strACSUrl = None, strIssuer = None):

        xSAMLPNode = ElementMaker(namespace='urn:oasis:names:tc:SAML:2.0:protocol', nsmap=dict(saml2p='urn:oasis:names:tc:SAML:2.0:protocol'))
        xSAMLNode = ElementMaker(namespace='urn:oasis:names:tc:SAML:2.0:assertion', nsmap=dict(saml2='urn:oasis:names:tc:SAML:2.0:assertion'))

        dCurrentTime = datetime.utcnow()

        xAuthnRequestNode = xSAMLPNode.AuthnRequest(ProtocolBinding='urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST', Version='2.0', IssueInstant= dCurrentTime.replace(microsecond=0).isoformat() + ".46Z", ID=uuid.uuid4().hex, AssertionConsumerServiceURL=strACSUrl)

        xIssuerNode = xSAMLNode.Issuer()
        xIssuerNode.text = strIssuer
        xAuthnRequestNode.append(xIssuerNode)

        xNameIDNode = xSAMLPNode.NameIDPolicy('urn:oasis:names:tc:SAML:2.0:nameid-format:unspecified',AllowCreate='true')
        xAuthnRequestNode.append(xNameIDNode)

        xAuthnContextNode = xSAMLPNode.RequestedAuthnContext(Comparison='exact')
        xAuthnRequestNode.append(xAuthnContextNode)
        xAuthnContextClassRef = xSAMLNode.AuthnContextClassRef()
        xAuthnContextClassRef.text = 'urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport'
        xAuthnContextNode.append(xAuthnContextClassRef)

        strBase64Request = base64.b64encode(etree.tostring(xAuthnRequestNode))
        strUrlParams = urllib.parse.urlencode([('SAMLRequest', strBase64Request)])
  
        return strUrlParams
      

class SAML_Response:
    def ParseSAMLResponse(strACSUrl, strEncodedSAMLResponse):

        cert = open("static/certificates/SignCertFromCentrify.cer").read()
        strDecodedSAMLResponse = b64decode(strEncodedSAMLResponse)
        authn_response = ""

        try:
            XMLVerifier().verify(strDecodedSAMLResponse, x509_cert=cert)
            
            root = etree.fromstring(b64decode(strEncodedSAMLResponse))
            
            strNameIdNode = root.xpath('//saml2p:Response/xmlns:Assertion/xmlns:Subject/xmlns:NameID', namespaces={'saml2p': 'urn:oasis:names:tc:SAML:2.0:protocol', 'xmlns': 'urn:oasis:names:tc:SAML:2.0:assertion'})

            strNameId = etree.tostring(strNameIdNode[0], method="text")

            authn_response = "SAML Response from IDP Was Accepted. Authenticated user is " + str(strNameId)[1:]

        except:
            authn_response = "SAML Response from IDP Was Not Accepted"

        return authn_response

