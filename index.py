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



        abc = ['BC','A','CD','AB','BA','TR','AEB','UTZ','ORT','QFE','AEB',
'RTU','CAB','RTA','AGL','AT','AIS','ABT','AC','AMS','ATS',
'BKN','BL','BR','BTN','CI','CNL','COR','COT','CS','CTA','CU',
'DA','DEG','DER','DME','DH','DP','DR','DS','DU','DZ','END',
'EST','ETA','FAF','FAP','FBL','FBW','FC','FEW','FG','FIR',
'FL','FM','FMC','FMS','FPM','FRG','FU','FZ','GND','GP','GR',
'GS','HL','HR','HVY','HZ','IAF','IAS','IC','ICE','IF','IFR',
'ILS','IM','IMC','ISA','LAN','LAT','LDG','LF',
'LLZ','LOC','LOM','LYR','MOC','MOD','MON','MOV','MPS','MSA',
'MSL','NSC','NSW','OBS','OVC','PAR','PDG','PIC','PL',
'PO','PR','PS','PSN','QNH','RA','RDH','RSR','RVR','RWY','SEV',
'SFC','SG','SH','SID','SKC','SLW','SM',
'SOC','SN','SQ','SQL','SS','SST','ST','SW','SWH','SWL','SWM',
'TAF','TAS','TC','UIR','UTC','VA','VAL','VC','VER','VFR','VIS',
'VKV','VOR','VPD','VRB','VSP','WKN','WMO']

        abc_l = filter(lambda s: len(s)<3, abc)
        abc_r = filter(lambda s: len(s)>=3, abc)


        mode=self.request.GET.get('mode','t')
        r = random.Random(int(seed))
        #r = random.Random()

    #    l1 = r.sample(string.ascii_uppercase,5)
    #    l2 = map(myjoin,r.sample(list(itertools.product(string.ascii_uppercase,repeat=2)),10))
    #    l = l1+l2
    #    r.shuffle(l)
    #    if 'OK' in l:
    #        l.remove('OK')
    #    l = r.sample(l,10)
    #    l3 = map(myjoin,r.sample(list(itertools.product(string.ascii_uppercase,repeat=3)),10))
    #    l.append('OK')
    #    l.extend(l3)
        
        l = r.sample(abc_l,10)
        l.append('OK')
        l.extend(r.sample(abc_r,10))


        query = []
        shift = r.sample(range(1,50),30)
        for i in range(1,30):
            query.extend(zip(zip(l,map(lambda x: x+i, shift)),itertools.repeat(False)))
            
        subquery = r.sample(range(0,len(query)),100)
        questions = []
        for s in subquery:
            query[s]=(query[s][0],True)
            questions.append(query[s][0])

        table = chunks(query,21)
        swap_mode = r.sample([True,False],1)[0]

         
        query_a = questions[:len(questions)/2]
        query_b = questions[len(questions)/2:]
        query = zip(query_a,query_b)

        



        template_values = {
            'seed': seed,
            'mode': mode,
            'swap': swap_mode,
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
