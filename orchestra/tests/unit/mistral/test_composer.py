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

from orchestra.composers import openstack
from orchestra.utils import plugin
from orchestra.tests.unit import base


class WorkflowComposerTest(base.WorkflowConductorTest):

    @classmethod
    def setUpClass(cls):
        cls.composer_name = 'mistral'
        super(WorkflowComposerTest, cls).setUpClass()

    def test_get_composer(self):
        self.assertEqual(
            plugin.get_module('orchestra.composers', self.composer_name),
            openstack.MistralWorkflowComposer
        )

    def test_exception_empty_definition(self):
        self.assertRaises(ValueError, self.composer.compose, {})
        self.assertRaises(ValueError, self.composer.compose, '')
        self.assertRaises(ValueError, self.composer.compose, None)