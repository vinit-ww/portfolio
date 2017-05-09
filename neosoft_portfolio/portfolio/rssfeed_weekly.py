import feedparser
import requests
import json


class RssReader(object):
	
    def text(self):
        d = feedparser.parse('http://localhost:8000/latest/comments/a112')
        context = {}
        html_content = []
        html_content.append("<table style='width:100%'>")
        for i,e in enumerate(d.entries):
            html_content.append("<tr><td>{}</td><td>{}</td><td><a href={} >\
                                 Link to Description</td></tr>".format(str(e.title),str(e.description),str(e.link)))
            
        html_content.append("</table>")
        html_content_str = ''.join(str(e) for e in html_content)

        return html_content_str 



