import cgi
import os
import re
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import mail
import settings

class About(webapp.RequestHandler):
  def get(self):
    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'about.html')
    self.response.out.write(template.render(path, template_values))

class MainPage(webapp.RequestHandler):
  def get(self):
  
    template_values = {
      'greetings': 'hi',
      }
	  
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    template_values = {
      'single_input' : cgi.escape(self.request.get('single_input')),
      'double_input' : cgi.escape(self.request.get('double_input')),
    }
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

    
class BenfordDouble(webapp.RequestHandler):
    def split_data(self, line):
        splitted = line.split(",")
        digit = ""
        if len(splitted) > 1:
            digit = re.sub("[^1-9]", "", splitted[1])
        if len(digit) > 0:
            return [splitted[0], digit[0]]
        else:
            return
        
    def get_table(self, posted_data):
        digits = range(1,10)
        benford = spread = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
        lines = posted_data.splitlines()
        #strip out lines that don't contain a character, comma, then digit
        data = map(self.split_data(), lines) #filter out non-numeric characters

    def post(self):
        posted = cgi.escape(self.request.get('content'))
        lines = posted.splitlines()
        message = ''
        set_names = ['Digits', 'Benford']
        
        table_data = [
            [1, 30.1],
            [2, 17.6],
            [3, 12.5],
            [4, 9.7],
            [5, 7.9],
            [6, 6.7],
            [7, 5.8],
            [8, 5.1],
            [9, 4.6],
        ]
        
    #    sets = {"Joe": [25, 9,4,3,2,1,2,2,1,1]}
        sets = {}
        totalcount = 0
        for line in lines:
            if line.find(',') == -1:
                continue
            values = line.split(',', 1)
            setname = values[0]
            num = re.sub("[^1-9]", "", values[1])
            if num.isdigit():
                if not sets.has_key(setname):
                    sets[setname] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    set_names.append(setname)
                 
                sets[setname][int(num[0])] += 1
                sets[setname][0] += 1
                totalcount += 1
                if totalcount == 10000:
                    message = 'The thousand number limit was reached.'
                    break
    
        for person in sets:
            person_count = sets[person][0]
            sets[person] = [elem * 100 / person_count for elem in sets[person]]
    
        for person in sets:
            table_data[0].append(sets[person][1])
            table_data[1].append(sets[person][2])
            table_data[2].append(sets[person][3])
            table_data[3].append(sets[person][4])
            table_data[4].append(sets[person][5])
            table_data[5].append(sets[person][6])
            table_data[6].append(sets[person][7])
            table_data[7].append(sets[person][8])
            table_data[8].append(sets[person][9])
    
        template_values = {
            'table_data': table_data,
            'set_names': set_names,
            'message': message,
            'input': posted,
        }
        
        path = os.path.join(os.path.dirname(__file__), 'double.html')
        self.response.out.write(template.render(path, template_values))
    
class BenfordSingle(webapp.RequestHandler):
    def get_table(self, posted_data):
        lines = posted_data.splitlines()
        lines = map(lambda x: re.sub("[^1-9]", "", x), lines) #filter out non-numeric characters
        lines = filter(lambda x: x.isdigit(), lines) #filter out potentially blank lines
        lines = map(lambda x: x[0], lines) #only take 1st
        spread = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
        discovered = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        for line in lines:
            discovered[int(line)-1] += 1
        numLines = len(lines)
        discovered = [elem * 100.0 / numLines for elem in discovered]

        table = map(lambda w, x, y: [w, x, y, abs(x-y)], range(1,10), spread, discovered)
        return table 

    def post(self):
        posted = cgi.escape(self.request.get('content'))
        table = self.get_table(posted)
        
        #1,2,3,4|4,5,6,7 <- series format
        series_data1, series_data2 = "", ""
        for row in table:
            series_data1 += str(row[1]) + ","
            series_data2 += str(row[2]) + ","
        #chart = "http://chart.apis.google.com/chart?chxl=1:|Leading+Digit+-+%25+Occurrence&chxp=1,30&chxr=0,1,9&chxs=0,676767,11.5,0,lt,676767|2,676767,11.5,0,lt,676767&chxt=x,x,y&chbh=a,5,20&chs=500x250&cht=bvg&chco=76A4FB,FF9900&chd=t:%s&chp=0&chm=D,4D89F9,0,0,5,1|D,FF9900,1,0,5" % (series_data1[0:-1] + "|" + series_data2[0:-1])
        chart_series = series_data1[0:-1] + "|" + series_data2[0:-1]
        #chart = "http://chart.apis.google.com/chart?chxr=0,1,9&chxs=0,676767,11.5,0,lt,676767&chxtc=0,1&chxt=x&chbh=a,5,20&chs=500x150&cht=bvg&chco=4D89F9,000000&chd=t:%s&chdl=Benford|Input+Data&chtt=Benford's+Law+Analysis" % (series_data1[0:-1] + "|" + series_data2[0:-1])

        template_values = {
          'table': table,
          'input': posted,
          'chart_series': chart_series,
          }
    
        path = os.path.join(os.path.dirname(__file__), 'single.html')
        self.response.out.write(template.render(path, template_values))

class ContactPage(webapp.RequestHandler):
    def get(self):
        template_values = {
                           'greetings': 'hi',
                           }
        path = os.path.join(os.path.dirname(__file__), 'contact.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        fromName = self.request.get('fromName')
        fromEmail = self.request.get('fromEmail')
        subject = 'Benford Email:' + self.request.get('subject')
        body = fromName + "\r\n" + fromEmail + "\r\n" + self.request.get('body')
    
        mail.send_mail(settings.EMAIL, settings.EMAIL, subject, body)

        template_values = {
                         'message' : '<p style="color: red;">Thank you for your feedback.</p>',
                         }
        path = os.path.join(os.path.dirname(__file__), 'contact.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/single', BenfordSingle),
                                      ('/double', BenfordDouble),
                                      ('/email', ContactPage),
                                      ('/about', About)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
