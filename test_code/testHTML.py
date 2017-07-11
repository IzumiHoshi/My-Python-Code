from html.parser import HTMLParser
from html.entities import name2codepoint


class MyHTMLParser(HTMLParser):

    def handle_starttag(slef, tag, attrs):
        print('handle_startag\t<%s %s>' % (tag, (attrs)))

    def handle_endtag(self, tag):
        print('handle_endtag\t</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('handle_startendtag\t<%s/>' % tag)

    def handle_data(self, data):
        print('handle_data\t%s' % data)

    def handle_comment(self, data):
        print('handle_comment\t<!--', data, '-->')

    def handle_entityref(self, name):
        print('handle_entityref\t&%s;' % name)

    def handle_charref(self, name):
        print('handle_charref\t&#%s;' % name)


parser = MyHTMLParser()
parser.feed('''<html><head></head><body><!-- test html parser --><p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p></body></html>''')