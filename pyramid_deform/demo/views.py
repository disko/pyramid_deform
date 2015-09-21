# -*- coding: utf-8 -*-

from pprint import pformat
from colander import Schema
from colander import SchemaNode
from colander import String
from deform.widget import TextAreaWidget
from pyramid.view import view_config
from pyramid_deform import FormWizard
from pyramid_deform import FormWizardView
from pyramid_deform import WizardState


class PageSchema(Schema):

    title = SchemaNode(String())
    description = SchemaNode(String(), widget=TextAreaWidget(), missing=u"")


class Wizard(FormWizard):
    def get_summary(self, request):
        result = []
        state = WizardState(request, self.name)
        step = state.get_step_num()
        last = len(self.schemas) - 1
        for num, schema in enumerate(self.schemas):
            classes = []
            is_first = num == 0
            is_last = num == last
            is_current = num == step
            if is_first:
                classes.append('first')
            if is_last:
                classes.append('last')
            if is_current:
                classes.append('active')
            result.append({
                'num': num,
                'name': schema.name,
                'title': schema.title,
                'desc': schema.description,
                'current': step == num,
                'url': request.path_url + '?step=%s' % num,
                'first': is_first,
                'last': is_last,
                'class': ' '.join(classes),
            })
        return result


@view_config(route_name='wizard', renderer='templates/form.pt')
class WizardView(FormWizardView):

    name = "wizard"
    schemas = (
        PageSchema(title='First Step'),
        PageSchema(title='Second Step'), )

    def __init__(self, request):
        self.request = request
        self.wizard = Wizard(self.name, self.done, *self.schemas)

    def __call__(self):
        result = super(WizardView, self).__call__(self.request)
        # result can either be:
        #   - a dictionary passed to the renderer or
        #   - a HTTPFound redirect
        if isinstance(result, dict):
            # Attach additional data to the result
            result['wizard'] = self.wizard
            result['summary'] = self.wizard.get_summary(self.request)
        return result

    def done(self, request, states):
        # Add your success handler here
        return {
            'appstruct': pformat(states),
        }
