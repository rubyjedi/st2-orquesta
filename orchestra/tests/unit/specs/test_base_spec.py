# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import six
import unittest

from orchestra import exceptions as exc
from orchestra.specs import types
from orchestra.tests.unit.specs import base as specs


class SpecTest(unittest.TestCase):

    def setUp(self):
        super(SpecTest, self).setUp()
        self.maxDiff = None

    def test_get_catalog(self):
        self.assertEqual(specs.MockSpec.get_catalog(), 'test')
        self.assertEqual(specs.MockMappingSpec.get_catalog(), 'test')
        self.assertEqual(specs.MockSequenceSpec.get_catalog(), 'test')

    def test_get_version(self):
        self.assertEqual('1.0', specs.MockSpec.get_version())

    def test_get_schema(self):
        schema = {
            'type': 'object',
            'properties': {
                'name': types.NONEMPTY_STRING,
                'version': types.VERSION,
                'description': types.NONEMPTY_STRING,
                'tags': types.UNIQUE_STRING_LIST,
                'inputs': types.UNIQUE_STRING_OR_ONE_KEY_DICT_LIST,
                'vars': types.NONEMPTY_DICT,
                'attr1': types.NONEMPTY_STRING,
                'attr1-1': types.NONEMPTY_STRING,
                'attr1_2': types.NONEMPTY_STRING,
                'attr2': types.NONEMPTY_DICT,
                'attr3': types.UNIQUE_STRING_LIST,
                'attr4': types.UNIQUE_STRING_OR_ONE_KEY_DICT_LIST,
                'attr5': specs.MockJointSpec.get_schema(includes=None),
                'attr6': specs.MockMappingSpec.get_schema(includes=None),
                'attr7': specs.MockSequenceSpec.get_schema(includes=None)
            },
            'required': ['attr1'],
            'additionalProperties': False
        }

        self.assertDictEqual(schema, specs.MockSpec.get_schema())

    def test_get_schema_specs_not_resolved(self):
        schema = {
            'type': 'object',
            'properties': {
                'name': types.NONEMPTY_STRING,
                'version': types.VERSION,
                'description': types.NONEMPTY_STRING,
                'tags': types.UNIQUE_STRING_LIST,
                'inputs': types.UNIQUE_STRING_OR_ONE_KEY_DICT_LIST,
                'vars': types.NONEMPTY_DICT,
                'attr1': types.NONEMPTY_STRING,
                'attr1-1': types.NONEMPTY_STRING,
                'attr1_2': types.NONEMPTY_STRING,
                'attr2': types.NONEMPTY_DICT,
                'attr3': types.UNIQUE_STRING_LIST,
                'attr4': types.UNIQUE_STRING_OR_ONE_KEY_DICT_LIST,
                'attr5': specs.MockJointSpec,
                'attr6': specs.MockMappingSpec,
                'attr7': specs.MockSequenceSpec
            },
            'required': ['attr1'],
            'additionalProperties': False
        }

        self.assertDictEqual(schema, specs.MockSpec.get_schema(resolve_specs=False))

    def test_get_schema_no_meta(self):
        schema = {
            'type': 'object',
            'properties': {
                'inputs': types.UNIQUE_STRING_OR_ONE_KEY_DICT_LIST,
                'vars': types.NONEMPTY_DICT,
                'attr1': types.NONEMPTY_STRING,
                'attr1-1': types.NONEMPTY_STRING,
                'attr1_2': types.NONEMPTY_STRING,
                'attr2': types.NONEMPTY_DICT,
                'attr3': types.UNIQUE_STRING_LIST,
                'attr4': types.UNIQUE_STRING_OR_ONE_KEY_DICT_LIST,
                'attr5': specs.MockJointSpec.get_schema(includes=None),
                'attr6': specs.MockMappingSpec.get_schema(includes=None),
                'attr7': specs.MockSequenceSpec.get_schema(includes=None)
            },
            'required': ['attr1'],
            'additionalProperties': False
        }

        self.assertDictEqual(schema, specs.MockSpec.get_schema(includes=None))

    def test_instance_schema(self):
        schema = {
            'type': 'object',
            'properties': {
                'inputs': types.UNIQUE_STRING_OR_ONE_KEY_DICT_LIST,
                'vars': types.NONEMPTY_DICT,
                'attr1': types.NONEMPTY_STRING,
                'attr1-1': types.NONEMPTY_STRING,
                'attr1_2': types.NONEMPTY_STRING,
                'attr2': types.NONEMPTY_DICT,
                'attr3': types.UNIQUE_STRING_LIST,
                'attr4': types.UNIQUE_STRING_OR_ONE_KEY_DICT_LIST,
                'attr5': specs.MockJointSpec,
                'attr6': specs.MockMappingSpec,
                'attr7': specs.MockSequenceSpec
            },
            'required': ['attr1'],
            'additionalProperties': False
        }

        self.assertDictEqual(schema, specs.MockSpec._schema)

    def test_spec_init_arg_none_type(self):
        self.assertRaises(
            ValueError,
            specs.MockSpec,
            None
        )

    def test_spec_init_arg_empty_str(self):
        self.assertRaises(
            ValueError,
            specs.MockSpec,
            ''
        )

    def test_spec_init(self):
        spec = {
            'name': 'mock',
            'version': '1.0',
            'description': 'This is a mock spec.',
            'inputs': [
                'x',
                {'y': 'polo'}
            ],
            'vars': {
                'var1': 'foobar',
                'var2': '<% $.x %>',
                'var3': '<% $.y %>'
            },
            'attr1': 'foobar',
            'attr1-1': 'fubar',
            'attr1_2': 'foosball',
            'attr2': {
                'macro': 'polo'
            },
            'attr3': [
                '<% $.var1 %>'
            ],
            'attr4': [
                {'open': 'sesame'},
                {'sesame': 'open'}
            ],
            'attr5': {
                'attr1': {
                    'attr1': '<% $.var2 %> <% $.var3 %>'
                }
            },
            'attr6': {
                'attr1': {
                    'attr1': {
                        'attr1': 'wunderbar'
                    }
                }
            },
            'attr7': [
                {
                    'attr1': {
                        'attr1': 'wunderbar'
                    }
                },
                {
                    'attr1': {
                        'attr1': 'wonderful'
                    }
                }
            ]
        }

        spec_obj = specs.MockSpec(spec)

        self.assertDictEqual(spec_obj.spec, spec)

        # Test properties from the meta schema.
        self.assertEqual(spec_obj.name, spec['name'])
        self.assertEqual(spec_obj.version, spec['version'])
        self.assertEqual(spec_obj.description, spec['description'])

        # Test simple properties from the schema.
        self.assertEqual(spec_obj.attr1, spec['attr1'])
        self.assertDictEqual(spec_obj.attr2, spec['attr2'])
        self.assertListEqual(spec_obj.attr3, spec['attr3'])

        # Test properties with dash or underscore in property name.
        self.assertEqual(spec_obj.attr1_1, spec['attr1-1'])
        self.assertEqual(getattr(spec_obj, 'attr1-1'), spec['attr1-1'])
        self.assertEqual(spec_obj.attr1_2, spec['attr1_2'])
        self.assertIsNone(getattr(spec_obj, 'attr1-2', None))

        # Test spec nesting.
        self.assertIsInstance(spec_obj.attr5, specs.MockJointSpec)
        self.assertIsInstance(spec_obj.attr5.attr1, specs.MockLeafSpec)

        self.assertEqual(
            spec_obj.attr5.attr1.attr1,
            spec['attr5']['attr1']['attr1']
        )

        # Test dictionary based spec class.
        self.assertIsInstance(spec_obj.attr6, specs.MockMappingSpec)
        self.assertIsInstance(spec_obj.attr6.attr1, specs.MockJointSpec)
        self.assertIsInstance(spec_obj.attr6.attr1.attr1, specs.MockLeafSpec)

        self.assertEqual(
            spec_obj.attr6.attr1.attr1.attr1,
            spec['attr6']['attr1']['attr1']['attr1']
        )

        attr6_keys = list(spec_obj.attr6.keys())
        attr6_values = list(spec_obj.attr6.values())
        attr6_items = list(spec_obj.attr6.items())
        attr6_iter = [item for item in spec_obj.attr6]
        attr6_iteritems = [(k, v) for k, v in six.iteritems(spec_obj.attr6)]

        self.assertListEqual(attr6_keys, ['attr1'])
        self.assertListEqual(attr6_values, [spec_obj.attr6.attr1])
        self.assertListEqual(attr6_items, [('attr1', spec_obj.attr6.attr1)])
        self.assertListEqual(attr6_iter, [('attr1', spec_obj.attr6.attr1)])
        self.assertListEqual(attr6_iteritems, [('attr1', spec_obj.attr6.attr1)])
        self.assertEqual(spec_obj.attr6['attr1'], spec_obj.attr6.attr1)

        # Test list based spec class.
        self.assertIsInstance(spec_obj.attr7, specs.MockSequenceSpec)
        self.assertEqual(len(spec_obj.attr7), 2)
        self.assertIsInstance(spec_obj.attr7[0], specs.MockJointSpec)
        self.assertIsInstance(spec_obj.attr7[1], specs.MockJointSpec)

        # Test non-existent attribute.
        self.assertRaises(AttributeError, getattr, spec_obj, 'attr9')

    def test_spec_serialize(self):
        spec = {
            'name': 'mock',
            'version': '1.0',
            'description': 'This is a mock spec.',
            'inputs': [
                'x',
                {'y': 'polo'}
            ],
            'vars': {
                'var1': 'foobar',
                'var2': '<% $.x %>',
                'var3': '<% $.y %>'
            },
            'attr1': 'foobar',
            'attr1-1': 'fubar',
            'attr1_2': 'foosball',
            'attr2': {
                'macro': 'polo'
            },
            'attr3': [
                '<% $.var1 %>'
            ],
            'attr4': [
                {'open': 'sesame'},
                {'sesame': 'open'}
            ],
            'attr5': {
                'attr1': {
                    'attr1': '<% $.var2 %> <% $.var3 %>'
                }
            },
            'attr6': {
                'attr1': {
                    'attr1': {
                        'attr1': 'wunderbar'
                    }
                }
            },
            'attr7': [
                {
                    'attr1': {
                        'attr1': 'wunderbar'
                    }
                },
                {
                    'attr1': {
                        'attr1': 'wonderful'
                    }
                }
            ]
        }

        spec_obj_1 = specs.MockSpec(spec)

        expected_data = {
            'catalog': spec_obj_1.get_catalog(),
            'version': spec_obj_1.get_version(),
            'name': spec_obj_1.name,
            'spec': spec_obj_1.spec
        }

        spec_obj_1_json = spec_obj_1.serialize()

        self.assertDictEqual(spec_obj_1_json, expected_data)

        spec_obj_2 = specs.MockSpec.deserialize(spec_obj_1_json)

        self.assertEqual(spec_obj_2.name, spec_obj_1.name)
        self.assertEqual(spec_obj_2.member, spec_obj_1.member)
        self.assertDictEqual(spec_obj_2.spec, spec_obj_1.spec)

    def test_spec_deserialize_errors(self):
        spec = {
            'name': 'mock',
            'version': '1.0',
            'description': 'This is a mock spec.',
            'inputs': [
                'x',
                {'y': 'polo'}
            ],
            'vars': {
                'var1': 'foobar',
                'var2': '<% $.x %>',
                'var3': '<% $.y %>'
            },
            'attr1': 'foobar',
            'attr1-1': 'fubar',
            'attr1_2': 'foosball',
            'attr2': {
                'macro': 'polo'
            },
            'attr3': [
                '<% $.var1 %>'
            ],
            'attr4': [
                {'open': 'sesame'},
                {'sesame': 'open'}
            ],
            'attr5': {
                'attr1': {
                    'attr1': '<% $.var2 %> <% $.var3 %>'
                }
            },
            'attr6': {
                'attr1': {
                    'attr1': {
                        'attr1': 'wunderbar'
                    }
                }
            },
            'attr7': [
                {
                    'attr1': {
                        'attr1': 'wunderbar'
                    }
                },
                {
                    'attr1': {
                        'attr1': 'wonderful'
                    }
                }
            ]
        }

        spec_obj = specs.MockSpec(spec)

        spec_obj_json = spec_obj.serialize()

        # Test missing catalog information.
        test_json = copy.deepcopy(spec_obj_json)
        test_json.pop('catalog')

        self.assertRaises(ValueError, specs.MockSpec.deserialize, test_json)

        # Test missing version information.
        test_json = copy.deepcopy(spec_obj_json)
        test_json.pop('version')

        self.assertRaises(ValueError, specs.MockSpec.deserialize, test_json)

        # Test mismatch version information.
        test_json = copy.deepcopy(spec_obj_json)
        test_json['version'] = '99.99'

        self.assertRaises(ValueError, specs.MockSpec.deserialize, test_json)

    def test_spec_init_name_not_given(self):
        spec = {
            'version': '1.0',
            'description': 'This is a mock spec.',
            'vars': {
                'var1': 'foobar',
                'var2': 'macro',
                'var3': 'polo'
            },
            'attr1': 'foobar'
        }

        spec_obj = specs.MockSpec(spec)

        self.assertDictEqual(spec_obj.spec, spec)
        self.assertIsNone(spec_obj.name)

    def test_spec_init_name_arg_given(self):
        spec = {
            'version': '1.0',
            'description': 'This is a mock spec.',
            'vars': {
                'var1': 'foobar',
                'var2': 'macro',
                'var3': 'polo'
            },
            'attr1': 'foobar'
        }

        spec_obj = specs.MockSpec(spec, name='mock')

        self.assertDictEqual(spec_obj.spec, spec)
        self.assertEqual(spec_obj.name, 'mock')

    def test_spec_init_just_required(self):
        spec = {
            'name': 'mock',
            'version': '1.0',
            'description': 'This is a mock spec.',
            'vars': {
                'var1': 'foobar',
                'var2': 'macro',
                'var3': 'polo'
            },
            'attr1': 'foobar'
        }

        spec_obj = specs.MockSpec(spec)

        self.assertDictEqual(spec_obj.spec, spec)
        self.assertEqual(spec_obj.name, spec['name'])
        self.assertEqual(spec_obj.version, spec['version'])
        self.assertEqual(spec_obj.description, spec['description'])
        self.assertEqual(spec_obj.attr1, spec['attr1'])
        self.assertIsNone(spec_obj.attr2)
        self.assertIsNone(spec_obj.attr3)
        self.assertIsNone(spec_obj.attr4)
        self.assertIsNone(spec_obj.attr5)
        self.assertIsNone(spec_obj.attr6)
        self.assertRaises(AttributeError, getattr, spec_obj, 'attr9')

    def test_spec_valid(self):
        spec = {
            'name': 'mock',
            'version': '1.0',
            'description': 'This is a mock spec.',
            'inputs': [
                'x',
                {'y': 'polo'}
            ],
            'vars': {
                'var1': 'foobar',
                'var2': '<% $.x %>',
                'var3': '<% $.y %>'
            },
            'attr1': 'foobar',
            'attr2': {
                'macro': 'polo'
            },
            'attr3': [
                '<% $.var1 %>'
            ],
            'attr4': [
                {'open': 'sesame'},
                {'sesame': 'open'}
            ],
            'attr5': {
                'attr1': {
                    'attr1': '<% $.var2 %> <% $.var3 %>'
                }
            }
        }

        spec_obj = specs.MockSpec(spec)

        self.assertDictEqual(spec_obj.spec, spec)
        self.assertDictEqual(spec_obj.inspect(), {})

    def test_spec_invalid(self):
        spec = {
            'name': 'mock',
            'version': None,
            'description': 'This is a mock spec.',
            'inputs': [
                'x',
                {'y': 'polo'}
            ],
            'vars': {
                'var1': 'foobar',
                'var2': '<% $.x %>',
                'var3': '<% $.y %>'
            },
            'attr2': {
                'macro': 'polo'
            },
            'attr3': [
                '<% 1 +/ 2 %> and <% {"a": 123} %>'
            ],
            'attr4': [
                {'var1': '<% $.fubar %>'}
            ],
            'attr5': {
                'attr1': {
                    'attr1': '<% <% $.var1 %> %>',
                    'attr2': '<% $.foobar %>'
                }
            }
        }

        errors = {
            'syntax': [
                {
                    'spec_path': 'version',
                    'schema_path': 'properties.version.anyOf',
                    'message': 'None is not valid under any '
                               'of the given schemas',
                },
                {
                    'spec_path': None,
                    'schema_path': 'required',
                    'message': '\'attr1\' is a required property'
                }
            ],
            'expressions': [
                {
                    'type': 'yaql',
                    'expression': '<% 1 +/ 2 %>',
                    'spec_path': 'attr3',
                    'schema_path': 'properties.attr3',
                    'message': 'Parse error: unexpected \'/\' at '
                               'position 3 of expression \'1 +/ 2\''
                },
                {
                    'type': 'yaql',
                    'expression': '<% {"a": 123} %>',
                    'spec_path': 'attr3',
                    'schema_path': 'properties.attr3',
                    'message': 'Lexical error: illegal character '
                               '\':\' at position 4',
                },
                {
                    'type': 'yaql',
                    'expression': '<% <% $.var1 %>',
                    'spec_path': 'attr5.attr1.attr1',
                    'schema_path': (
                        'properties.attr5.'
                        'properties.attr1.'
                        'properties.attr1'
                    ),
                    'message': 'Parse error: unexpected \'<\' at position 0 '
                               'of expression \'<% $.var1\''
                }
            ],
            'context': [
                {
                    'type': 'yaql',
                    'expression': '<% $.fubar %>',
                    'spec_path': 'attr4',
                    'schema_path': 'properties.attr4',
                    'message': 'Variable "fubar" is referenced '
                               'before assignment.'
                },
                {
                    'type': 'yaql',
                    'expression': '<% $.foobar %>',
                    'spec_path': 'attr5.attr1.attr2',
                    'schema_path': (
                        'properties.attr5.'
                        'properties.attr1.'
                        'properties.attr2'
                    ),
                    'message': 'Variable "foobar" is referenced '
                               'before assignment.'
                }
            ]
        }

        spec_obj = specs.MockSpec(spec)

        self.assertDictEqual(spec_obj.inspect(), errors)

    def test_spec_invalid_raise_exception(self):
        spec = {
            'name': 'mock',
            'version': None,
            'description': 'This is a mock spec.',
            'inputs': [
                'x',
                {'y': 'polo'}
            ],
            'vars': {
                'var1': 'foobar',
                'var2': '<% $.x %>',
                'var3': '<% $.y %>'
            },
            'attr2': {
                'macro': 'polo'
            },
            'attr3': [
                '<% 1 +/ 2 %> and <% {"a": 123} %>'
            ],
            'attr4': [
                {'var1': '<% $.fubar %>'}
            ],
            'attr5': {
                'attr1': {
                    'attr1': '<% <% $.var1 %> %>',
                    'attr2': '<% $.foobar %>'
                }
            }
        }

        errors = {
            'syntax': [
                {
                    'spec_path': 'version',
                    'schema_path': 'properties.version.anyOf',
                    'message': 'None is not valid under any '
                               'of the given schemas',
                },
                {
                    'spec_path': None,
                    'schema_path': 'required',
                    'message': '\'attr1\' is a required property'
                }
            ],
            'expressions': [
                {
                    'type': 'yaql',
                    'expression': '<% 1 +/ 2 %>',
                    'spec_path': 'attr3',
                    'schema_path': 'properties.attr3',
                    'message': 'Parse error: unexpected \'/\' at '
                               'position 3 of expression \'1 +/ 2\''
                },
                {
                    'type': 'yaql',
                    'expression': '<% {"a": 123} %>',
                    'spec_path': 'attr3',
                    'schema_path': 'properties.attr3',
                    'message': 'Lexical error: illegal character '
                               '\':\' at position 4',
                },
                {
                    'type': 'yaql',
                    'expression': '<% <% $.var1 %>',
                    'spec_path': 'attr5.attr1.attr1',
                    'schema_path': (
                        'properties.attr5.'
                        'properties.attr1.'
                        'properties.attr1'
                    ),
                    'message': 'Parse error: unexpected \'<\' at position 0 '
                               'of expression \'<% $.var1\''
                }
            ],
            'context': [
                {
                    'type': 'yaql',
                    'expression': '<% $.fubar %>',
                    'spec_path': 'attr4',
                    'schema_path': 'properties.attr4',
                    'message': 'Variable "fubar" is referenced '
                               'before assignment.'
                },
                {
                    'type': 'yaql',
                    'expression': '<% $.foobar %>',
                    'spec_path': 'attr5.attr1.attr2',
                    'schema_path': (
                        'properties.attr5.'
                        'properties.attr1.'
                        'properties.attr2'
                    ),
                    'message': 'Variable "foobar" is referenced '
                               'before assignment.'
                }
            ]
        }

        spec_obj = specs.MockSpec(spec)

        with self.assertRaises(exc.WorkflowInspectionError) as ctx:
            spec_obj.inspect(raise_exception=True)

        self.assertEqual(len(ctx.exception.args), 2)
        self.assertEqual(ctx.exception.args[0], 'Workflow definition failed inspection.')
        self.assertDictEqual(ctx.exception.args[1], errors)
