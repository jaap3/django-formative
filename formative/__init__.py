from formative.registry import autodiscover, register
from formative.registry import FormativeTypeRegistry

__version__ = '0.1.0'
__ = [autodiscover, register]
registry = FormativeTypeRegistry()
