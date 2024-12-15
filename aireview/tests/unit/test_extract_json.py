import unittest

from aireview.utils.extract_json import extract_json


class TestExtractJson(unittest.TestCase):
    def test_single_json(self):
        text = 'Some text before {"sha": "951b12a93e1ade83bce9d18c4d240bfa2f9d3067", "file_path": "/path/to/file", "line": "19", "content": "Consider adding error handling around the submit_review call since it\'s an async operation that could fail. Wrap with try-except and log errors.", "type": "example"} some text after'
        result = extract_json(text)
        expected = [{"sha": "951b12a93e1ade83bce9d18c4d240bfa2f9d3067", "file_path": "/path/to/file", "line": "19", "content": "Consider adding error handling around the submit_review call since it's an async operation that could fail. Wrap with try-except and log errors.", "type": "example"}]
        self.assertEqual(result, expected)

    def test_multiple_json(self):
        text = ('Some text before '
                '{"file_path": "/path/to/file1", "type": "example1"}'
                ' middle text '
                '{"file_path": "/path/to/file2", "type": "example2"}'
                ' after text')
        result = extract_json(text)
        expected = [
            {"file_path": "/path/to/file1", "type": "example1"},
            {"file_path": "/path/to/file2", "type": "example2"}
        ]
        self.assertEqual(result, expected)

    def test_valid_json_with_comments(self):
        text = ('{'
                '"sha": "951b12a93e1ade83bce9d18c4d240bfa2f9d3067",'
                '"file_path": "aireview/src/aireview/application/controllers/review_controller.py",'
                '"line": "19",'
                '"content": "Consider adding error handling around the submit_review call since it\'s an async operation that could fail. Wrap with try-except and log errors.",'
                '"type": "style"'
                '}')
        result = extract_json(text)
        expected = [{"sha": "951b12a93e1ade83bce9d18c4d240bfa2f9d3067", "file_path": "aireview/src/aireview/application/controllers/review_controller.py", "line": "19", "content": "Consider adding error handling around the submit_review call since it's an async operation that could fail. Wrap with try-except and log errors.", "type": "style"}]
        self.assertEqual(result, expected)


    def test_nested_json_list(self):
        text = '[{"sha": "951b12a93e1ade83bce9d18c4d240bfa2f9d3067", "file_path": "aireview/src/aireview/domain/services/code_analyzer.py", "line": 19, "content": "Debug print statements should be removed from production code. Consider using a proper logging framework like Python\'s built-in \'logging\' module instead.", "type": "style"}, {"sha": "951b12a93e1ade83bce9d18c4d240bfa2f9d3067", "file_path": "aireview/src/aireview/domain/services/code_analyzer.py", "line": 7, "content": "Return type \'Review\' with hardcoded values (1, \'summary of review\', \'COMMENT\') suggests tight coupling. Consider making these values configurable or derived from the analysis results.", "type": "style"}, {"sha": "951b12a93e1ade83bce9d18c4d240bfa2f9d3067", "file_path": "aireview/src/aireview/domain/services/code_analyzer.py", "line": 35, "content": "Good improvement replacing hardcoded ReviewComment with dynamic parsing from JSON, following better separation of concerns.", "type": "style"}]'
        result = extract_json(text)
        expected = [
            {"sha": "951b12a93e1ade83bce9d18c4d240bfa2f9d3067", "file_path": "aireview/src/aireview/domain/services/code_analyzer.py", "line": 19,
             "content": "Debug print statements should be removed from production code. Consider using a proper logging framework like Python's built-in 'logging' module instead.",
             "type": "style"},
            {"sha": "951b12a93e1ade83bce9d18c4d240bfa2f9d3067", "file_path": "aireview/src/aireview/domain/services/code_analyzer.py", "line": 7,
             "content": "Return type 'Review' with hardcoded values (1, 'summary of review', 'COMMENT') suggests tight coupling. Consider making these values configurable or derived from the analysis results.",
             "type": "style"},
            {"sha": "951b12a93e1ade83bce9d18c4d240bfa2f9d3067", "file_path": "aireview/src/aireview/domain/services/code_analyzer.py", "line": 35,
             "content": "Good improvement replacing hardcoded ReviewComment with dynamic parsing from JSON, following better separation of concerns.",
             "type": "style"}
        ]
        self.assertEqual(expected, result)

    def test_edge_case(self):
        text = '{"file_path": "some/path", "type": "test"}text without separator'
        result = extract_json(text)
        expected = [{"file_path": "some/path", "type": "test"}]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
