import webapp2
import os
import urllib2
from google.appengine.ext import db
import jinja2
import urlparse

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',0,1,2,3,4,5,6,7,8,9]
class StoreUrl(db.Model):
    lurl = db.StringProperty(required=True)


class MainHandler(BaseHandler):
    def get(self):
        self.render('welcome.html')
    def post(self):
        lurl = self.request.get('lurl')
        lurl_instance = StoreUrl(lurl=lurl)
        lurl_instance.put()
        k = lurl_instance.key()
        idd = k.id() #Here comes the ID of the stored url which I needed the most!
        #This ID which is in deciml form should be converted into BASE62 form!
        #Below is the algorithm of conversion.
        idd_c = idd%1000000
        id_list = []
        while(idd_c > 0):
            rem = idd_c%62
            id_list.append(rem)
            idd_c = idd_c/62
        id_list.reverse()
        i=0
        final_url = "http://url-s123.appspot.com/"
        while i<len(id_list):
            x = alphabets[id_list[i]]
            i = i+1
            final_url = final_url + str(x)
        j = StoreUrl.get_by_id(idd)
        redirection_url = j.lurl
        self.render('results.html',redirection_url=redirection_url,final_url=final_url)

        #We have got the shortened url! Now the task is to link it to the long url:D
        short_path_id = [] #List to store the six digits of the ID by reverse lookup through path of the shortened url.
        path = urlparse.urlparse(final_url).path
        j = 1
        while j<len(path):
            try:
                short_path_id.append(alphabets.index(path[j]))
                j = j + 1
            except ValueError:
                short_path_id.append(alphabets.index(int(path[j])))
                j = j + 1
        self.response.out.write(short_path_id)
        



    
    

















        
        
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
