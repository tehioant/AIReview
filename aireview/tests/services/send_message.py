import unittest
from pyexpat.errors import messages


class MyTestCase(unittest.TestCase):
    def given_message_when_send_to_dust_then_send_message(self):
        message = "hello my message"

        dust_agent.send(message)

        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
