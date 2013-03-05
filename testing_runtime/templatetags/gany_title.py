#from django import template
#
#register = template.Library()
#
#class FormatNode(template.Node):
#    def __init__(self, format_string):
#        self.format_string = format_string
#
#    def render(self, context):
#        return self.format_string
#
#def cut(parser, arg):
#    q1, q2 = arg.split_contents()
#    return FormatNode(q2)
#
#register.tag("cut", cut)