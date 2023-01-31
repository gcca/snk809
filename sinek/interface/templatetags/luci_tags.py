from typing import List

from django.template import Library, Node
from django.template.library import token_kwargs

from sinek.interface.site import imgs

register = Library()


@register.inclusion_tag('desktop/common/tags/typeahead.html')
def luci_typeahead(name: str, areas: List[str], allAreas: List[str] = None):
  backgroundColor = {
    'business': '#2CA8FF',
    'project': '#3C64B1',
  }
  placeholder = {
    'business': 'rubros',
    'project': 'tipos de proyecto',
  }

  return {
    'name': name,
    'placeholder': placeholder[name],
    'areas': areas,
    'allAreas': allAreas,
    'color': backgroundColor[name],
    'icon': imgs.SEARCH_ICON,
  }


@register.inclusion_tag('desktop/common/tags/slimselect.html')
def luci_slimselect(name: str, options: List[str], selectedOptions: List[str]):
  backgroundColor = {
    'businesses': '#3C64B1',
    'projects': '#2CA8FF',
    'knowledges': '#FF70A9',
  }
  placeholder = {
    'businesses': 'Seleccione más rubros',
    'projects': 'Seleccione más tipos',
    'knowledges': 'Seleccione más servicios',
  }

  return {
    'name': name,
    'placeholder': placeholder[name],
    'options': options,
    'selectedOptions': selectedOptions,
    'color': backgroundColor[name],
  }


@register.inclusion_tag('desktop/common/tags/freelancer-slimselect.html')
def luci_freelancer_slimselect(
    name: str, options: List[str],
    selectedOptions: List[str]):
  backgroundColor = {
    'businesses': '#3C64B1',
    'projects': '#2CA8FF',
  }
  placeholder = {
    'businesses': 'Agregar rubros en los que he trabajado',
    'projects': 'Agregar tipos de proyectos en los que he trabajado',
  }

  return {
    'name': name,
    'placeholder': placeholder[name],
    'options': options,
    'selectedOptions': selectedOptions,
    'color': backgroundColor[name],
  }


@register.tag
def luci_tabs(parser, token):
  nodelist = parser.parse(('end_luci_tabs',))
  parser.delete_first_token()
  return TabsNode(nodelist)


class TabsNode(Node):

  def __init__(self, nodelist):
    self.nodelist = nodelist

  def render(self, context):
    import uuid
    context['luci_tabs_id'] = uuid.uuid1().hex
    output = self.nodelist.render(context)

    return f'<div class="tabs">{output}</div>'


# TODO: crear un sinek_tab_selected para evitar condicional
@register.tag
def luci_tab(parser, token):
  bits = token.split_contents()
  kwargs = token_kwargs(bits[1:], parser)
  nodelist = parser.parse(('end_luci_tab',))
  parser.delete_first_token()
  return TabNode(nodelist, kwargs)


tabcounter = 0


class TabNode(Node):

  def __init__(self, nodelist, kwargs):
    self.nodelist = nodelist
    self.kwargs = kwargs

  def render(self, context):
    global tabcounter
    output = self.nodelist.render(context)
    name = context['luci_tabs_id']
    tabcounter += 1

    kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}
    title = kwargs.get('title', '')
    eid = kwargs.get('id')
    selected = kwargs.get('selected', False)

    return f'''
    <div {f'id={eid}' if eid else ''} class="tab">
      <input type="radio" name="tab-group-{name}" value="{tabcounter}" id="tab-tribe-info-{tabcounter}" { 'checked' if selected else ''}>
      <label for="tab-tribe-info-{tabcounter}"><span>{title}</span></label>
      <div class="tab-content">
      {output}
      </div>
    </div>
    '''
