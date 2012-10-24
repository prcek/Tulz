import webapp2
import jinja2
import os
import random
import string
import itertools

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))



def myjoin(iterable):
    return string.join(iterable,sep='')


class MainPage(webapp2.RequestHandler):
    def get(self):
    
        #r = random.Random(2)
        r = random.Random()

        l1 = r.sample(string.ascii_uppercase,5)
        l2 = map(myjoin,r.sample(list(itertools.product(string.ascii_uppercase,repeat=2)),10))
        l = l1+l2
        r.shuffle(l)
        l = r.sample(l,9)
        l3 = map(myjoin,r.sample(list(itertools.product(string.ascii_uppercase,repeat=3)),10))
        l.append('OK')
        l.extend(l3)
        table = []
        for i in range(1,41):
            lr = map(string.join,zip(l,itertools.repeat(str(i))))
            table.append(lr)
        
        template_values = {
            'table': table,
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))
  
app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
