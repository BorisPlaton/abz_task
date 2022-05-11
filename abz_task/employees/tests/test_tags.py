from django.test import TestCase

from employees.templatetags.pagination_tags import url_parameters, is_int


class CustomTemplateTagsTests(TestCase):

    def test_url_parameters_tag_without_arguments(self):
        parameter_string = url_parameters()
        self.assertEqual(parameter_string, '')

    def test_url_parameters_tag_with_position_params_argument(self):
        parameter_string = url_parameters({'some_parameter': 'some string'})
        self.assertEqual(parameter_string, '?some_parameter=some-string')

    def test_url_parameters_tag_with_position_params_argument_multiple_value(self):
        parameter_string = url_parameters(
            {
                'some_parameter': 'some string',
                'some_new_parameter': 'woa11111h',
                'nothing': '',
            }
        )
        self.assertEqual(parameter_string, '?some_parameter=some-string&some_new_parameter=woa11111h')

    def test_url_parameters_tag_with_position_params_argument_multiple_value_and_kwargs(self):
        parameter_string = url_parameters(
            {
                'some_parameter': 'some string',
                'some_new_parameter': 'woa11111h',
                'nothing': '',
            },
            kwargs_value='some_new'
        )
        self.assertEqual(
            parameter_string,
            '?kwargs_value=some_new&some_parameter=some-string&some_new_parameter=woa11111h'
        )

    def test_url_parameters_tag_with_kwargs_values(self):
        parameter_string = url_parameters(
            kwargs_value='some_new',
            empty_value='',
            some_new_value='notemptyvalue'
        )
        self.assertEqual(parameter_string, '?kwargs_value=some_new&some_new_value=notemptyvalue')

    def test_is_int_filter_with_list_argument(self):
        is_int_value = is_int([2, 2, 3])
        self.assertFalse(is_int_value)

    def test_is_int_filter_with_string_argument(self):
        is_int_value = is_int("not int")
        self.assertFalse(is_int_value)

    def test_is_int_filter_with_float_argument(self):
        is_int_value = is_int(2.0)
        self.assertFalse(is_int_value)

    def test_is_int_filter_without_argument(self):
        is_int_value = is_int()
        self.assertFalse(is_int_value)

    def test_is_int_filter_with_int_argument(self):
        is_int_value = is_int(1)
        self.assertTrue(is_int_value)
