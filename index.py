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

def chunks(thing, chunk_length):
    for i in xrange(0, len(thing), chunk_length):
        yield thing[i:i+chunk_length]

class MainPage(webapp2.RequestHandler):
    def get(self, seed=None):
        if seed is None:
            return webapp2.redirect('/%d' % (random.randrange(0,100000)))

        #if (mode is None) or not (mode in ['t','e','a']):
        #    mode = 't'
        #    return webapp2.redirect('/%s/%s' % (seed,mode))    

        mode=self.request.GET.get('mode','t')
        r = random.Random(int(seed))
        #r = random.Random()

        l1 = r.sample(string.ascii_uppercase,5)
        l2 = map(myjoin,r.sample(list(itertools.product(string.ascii_uppercase,repeat=2)),10))
        l = l1+l2
        r.shuffle(l)
        if 'OK' in l:
            l.remove('OK')
        l = r.sample(l,9)
        l3 = map(myjoin,r.sample(list(itertools.product(string.ascii_uppercase,repeat=3)),10))
        l.append('OK')
        l.extend(l3)
        



        query = []
        for i in range(1,41):
            query.extend(zip(zip(l,itertools.repeat(str(i))),itertools.repeat(False)))
            
        subquery = r.sample(range(0,len(query)),100)
        questions = []
        for s in subquery:
            query[s]=(query[s][0],True)
            questions.extend(query[s])

        table = chunks(query,20)


        query_a = questions[:len(questions)/2]
        query_b = questions[len(questions)/2:]
        query = zip(query_a,query_b)

        template_values = {
            'seed': seed,
            'mode': mode,
            'table': table,
            'query': query,
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))
  
app = webapp2.WSGIApplication([
    (r'/', MainPage),
    (r'/(\d+)',MainPage),
    ],
    debug=True)
