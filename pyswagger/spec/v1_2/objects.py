from __future__ import absolute_import
from ...base import BaseObj, FieldMeta, Context
import six
import copy


class Items(six.with_metaclass(FieldMeta, BaseObj)):
    """ Items Object
    """
    __swagger_fields__ = [
        ('$ref', None),
        ('type', None),
        ('format', None),
    ]


class ItemsContext(Context):
    """ Context of Items Object
    """
    __swagger_ref_object__ = Items


class DataTypeObj(BaseObj):
    """ Data Type Fields
    """
    __swagger_fields__ = [
        ('type', None),
        ('$ref', None),
        ('format', None),
        ('defaultValue', None),
        ('enum', None),
        ('items', None),
        ('minimum', None),
        ('maximum', None),
        ('uniqueItems', None),
    ]

    def __init__(self, ctx):
        # Items Object, too lazy to create a Context for DataTypeObj
        # to wrap this child.
        items_data = ctx._obj.get('items', None)
        if items_data:
            with ItemsContext(ctx._obj, 'items') as items_ctx:
                items_ctx.parse(items_data)
        else:
            setattr(self, self.get_private_name('items'), None)

        # TODO: duplicate code in BaseObj.__init__
        for name, default in DataTypeObj.__swagger_fields__:
            # almost every data field is not required.
            setattr(self, self.get_private_name(name), ctx._obj.get(name, copy.copy(default)))

        super(DataTypeObj, self).__init__(ctx)

class Scope(six.with_metaclass(FieldMeta, BaseObj)):
    """ Scope Object
    """

    __swagger_fields__ = [
        ('scope', None),
    ]


class LoginEndpoint(six.with_metaclass(FieldMeta, BaseObj)):
    """ LoginEndpoint Object
    """

    __swagger_fields__ = [
        ('url', None),
    ]


class Implicit(six.with_metaclass(FieldMeta, BaseObj)):
    """ Implicit Object
    """

    __swagger_fields__ = [
        ('loginEndpoint', None),
        ('tokenName', None),
    ]


class TokenRequestEndpoint(six.with_metaclass(FieldMeta, BaseObj)):
    """ TokenRequestEndpoint Object
    """

    __swagger_fields__ = [
        ('url', None),
        ('clientIdName', None),
        ('clientSecretName', None),
    ]


class TokenEndpoint(six.with_metaclass(FieldMeta, BaseObj)):
    """ TokenEndpoint Object
    """

    __swagger_fields__ = [
        ('url', None),
        ('tokenName', None),
    ]


class AuthorizationCode(six.with_metaclass(FieldMeta, BaseObj)):
    """ AuthorizationCode Object
    """

    __swagger_fields__ = [
        ('tokenRequestEndpoint', None),
        ('tokenEndpoint', None),
    ]


class GrantType(six.with_metaclass(FieldMeta, BaseObj)):
    """ GrantType Object
    """

    __swagger_fields__ = [
        ('implicit', None),
        ('authorization_code', None),
    ]


class Authorizations(six.with_metaclass(FieldMeta, BaseObj)):
    """ Authorizations Object
    """

    __swagger_fields__ = [
        ('scope', None),
    ]


class Authorization(six.with_metaclass(FieldMeta, BaseObj)):
    """ Authorization Object
    """

    __swagger_fields__ = [
        ('type', None),
        ('passAs', None),
        ('keyname', None),
        ('scopes', None),
        ('grantTypes', None),
    ]

    def get_name(self, path):
        return path.split('/', 3)[2]


class ResponseMessage(six.with_metaclass(FieldMeta, BaseObj)):
    """ ResponseMessage Object
    """

    __swagger_fields__ = [
        ('code', None),
        ('message', None),
        ('responseModel', None),
    ]


class Parameter(six.with_metaclass(FieldMeta, DataTypeObj)):
    """ Parameter Object
    """

    __swagger_fields__ = [
        ('paramType', None),
        ('name', None),
        ('required', None),
        ('allowMultiple', None),
    ]


class Operation(six.with_metaclass(FieldMeta, DataTypeObj)):
    """ Operation Object
    """

    __swagger_fields__ = [
        ('method', None),
        ('nickname', None),
        ('authorizations', None),
        ('parameters', None),
        ('responseMessages', None),
        ('produces', None),
        ('consumes', None),
        ('deprecated', None),

        # path from Api object, concated with Resource object
        ('path', None),
    ]

    def get_name(self, path):
        return self.nickname


class Api(six.with_metaclass(FieldMeta, BaseObj)):
    """ Api Object
    """

    __swagger_fields__ = [
        ('path', None),
        ('operations', None),
    ]


class Property(six.with_metaclass(FieldMeta, DataTypeObj)):
    """ Property Object
    """

    __swagger_fields__ = []


class Model(six.with_metaclass(FieldMeta, BaseObj)):
    """ Model Object
    """

    __swagger_fields__ = [
        ('id', None),
        ('required', None),
        ('properties', None),
        ('subTypes', None),
        ('discriminator', None),

        # for model inheritance
        ('_extends_', None),
        ]

    def get_name(self, path):
        return self.id


class Resource(six.with_metaclass(FieldMeta, BaseObj)):
    """ Resource Object
    """

    __swagger_fields__ = [
        ('swaggerVersion', None),
        ('apiVersion', None),
        ('apis', None),
        ('basePath', None),
        ('resourcePath', None),
        ('models', None),
        ('produces', None),
        ('consumes', None),
        ('authorizations', None),
    ]

    def __init__(self, ctx):
        """ The original structure of API object is very bad
        for seeking nickname for operations. Since nickname is unique
        in one Resource, we can just make it flat.
        """
        super(Resource, self).__init__(ctx)

        new_api = {}
        for api in ctx._obj['apis']:
            for op in api.operations:
                name = op.nickname
                if name in new_api.keys():
                    raise ValueError('duplication operation found: ' + name)

                # Operation objects now have 'path' attribute.
                op.update_field('path', api.path)
                # Operation objects' parent is now Resource object(API Declaration).
                op._parent__ = self
                new_api[name] = op

        # replace Api with Operations
        self.update_field('apis', new_api)

    def get_name(self, path):
        return path.split('/', 3)[2]


class Info(six.with_metaclass(FieldMeta, BaseObj)):
    """ Info Object
    """

    __swagger_fields__ = [
        ('title', None),
        ('termsOfServiceUrl', None),
        ('contact', None),
        ('license', None),
        ('licenseUrl', None),
        ('description', None),
    ]


class ResourceList(six.with_metaclass(FieldMeta, BaseObj)):
    """ Resource List Object
    """
    __swagger_fields__ = [
        ('swaggerVersion', None),
        ('apis', None),
        ('apiVersion', None),
        ('info', None),
        ('authorizations', None),
    ]

