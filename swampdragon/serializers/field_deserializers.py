from abc import ABCMeta, abstractmethod
from dateutil.parser import parse
from django.utils import six


deserializer_map = {}


def register_field_deserializer(field_name, deserializer):
    deserializer_map[field_name] = deserializer


class BaseFieldDeserializer(six.with_metaclass(ABCMeta, object)):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class DateTimeDeserializer(BaseFieldDeserializer):
    def __call__(self, model_instance, key, val):
        date_val = parse(val)
        setattr(model_instance, key, date_val)


class DateDeserializer(DateTimeDeserializer):
    pass


register_field_deserializer('DateTimeField', DateTimeDeserializer)
register_field_deserializer('DateField', DateDeserializer)


def get_deserializer(name):
    if name in deserializer_map:
        return deserializer_map[name]()
    return None
