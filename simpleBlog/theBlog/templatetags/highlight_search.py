from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()
@register.filter
def highlight_search_body(text, search):
    matched = re.findall(search,text,flags=re.IGNORECASE)
    if matched:
        matched = list(dict.fromkeys(matched))
        # print(matched)
        # highlighted = text
        # for match in matched:
        #     highlighted = highlighted.replace(match, '<mark>{}</mark>'.format(match))
        # print(highlighted.split(search))
        lines = text.split('\n')
        highlighted = ''
        for line in lines:
            has_match = False
            for match in matched:
                if match in line:
                    has_match = True
                    line = line.replace(match, '<mark>{}</mark>'.format(match))
            if has_match:
                highlighted = highlighted + line + "<br>...<br>" 
        # print(highlighted)
        return mark_safe(highlighted)
    else:
        return mark_safe('')

@register.filter
def highlight_search_title(text, search):
    matched = re.findall(search,text,flags=re.IGNORECASE)
    if matched:
        matched = list(dict.fromkeys(matched))
        # print(matched)
        highlighted = text
        for match in matched:
            highlighted = highlighted.replace(match, '<mark>{}</mark>'.format(match))
        
        return mark_safe(highlighted)
    else:
        return mark_safe(text)    