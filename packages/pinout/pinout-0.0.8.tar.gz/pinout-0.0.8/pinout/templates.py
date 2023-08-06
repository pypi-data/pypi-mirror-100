from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader('pinout','templates'),
    autoescape=select_autoescape(['html', 'xml']),
)

env.trim_blocks = True
env.lstrip_blocks = True

# Base SVG elements
svg = env.get_template('svg.svg')
svg_group = env.get_template('group.svg')
svg_image = env.get_template('image.svg')
svg_style = env.get_template('style.svg')

# CSS styles
stylesheet = env.get_template('stylesheet.css')

# Component SVG templates (made from multiple svg elements)
svg_legend = env.get_template('legend.svg')
svg_label = env.get_template('label.svg')
svg_pin = env.get_template('pin.svg')
