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
        digits = ["Digits"] + range(1,10)
        benford = ["Benford"] + [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
        lines = posted_data.splitlines()
        #strip out lines that don't contain a character, comma, then digit
        data = map(self.split_data, lines)
        data = filter(lambda x: x, data)
        people_data = {} # "Jim" = [1, 0, 1, 2, 3, 1, 0, 0, 9]
        for item in data:
            if not people_data.has_key(item[0]):
                people_data[item[0]] = [0,0,0,0,0,0,0,0,0]
            people_data[item[0]][int(item[1])-1] += 1
        formatted_data = [] # [Jim, 30.1, 30.2, 30.3 ...]
        for key, value in sorted(people_data.iteritems()):
            distribution = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            for i in range(1, 10):
                distribution[i-1] = (value[i-1] * 100.0) / (sum(value) * 1.0)
            arr = [key.encode('ascii')] #necessary b/c this is stored as unicode
            arr.extend(distribution)
            formatted_data += [arr]
        table = [digits, benford]
        for row in formatted_data:
            table.append(row)
        return table
       
       
    def post(self):
        posted = cgi.escape(self.request.get('content'))
        table_data = self.get_table(posted)
        flip_table = zip(*table_data)
        
        template_values = {
            'table_data': flip_table,
            'input': posted,
            'chart_data': str(table_data[1:]),
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
        chart_series = series_data1[0:-1] + "|" + series_data2[0:-1]

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
