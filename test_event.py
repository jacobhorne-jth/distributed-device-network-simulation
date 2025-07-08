import unittest
from device import Device
from event import Event
import contextlib
import io

class EventClassTest(unittest.TestCase):
    def test_event_object_creation(self) -> None:
        test_sender_device = Device(1, 500)
        test_receiver_device = Device(2, 500)
        test_event = Event(test_sender_device, test_receiver_device, 'ALERT', 'Trouble', 0, 'S')
        self.assertEqual(test_event.get_sender(), test_sender_device)
        self.assertEqual(test_event.get_receiver(), test_receiver_device)
        self.assertEqual(test_event.get_event_type(), 'ALERT')
        self.assertEqual(test_event.get_description(), 'Trouble')
        self.assertEqual(test_event.get_time(), 0)
        self.assertEqual(test_event.get_phase(), 'S')

    def test_log_receive(self) -> None:
        test_sender_device = Device(2, 500)
        test_receiver_device = Device(3, 500)
        test_event = Event(test_sender_device, test_receiver_device, 'ALERT', 'Trouble', 0, 'S')
        with contextlib.redirect_stdout(io.StringIO()) as output:
            test_event.log()
        self.assertEqual(output.getvalue(), "@0: #2 SENT ALERT TO #3: Trouble\n")

    def test_log_send(self) -> None:
        test_sender_device = Device(2, 500)
        test_receiver_device = Device(3, 500)
        test_event = Event(test_sender_device, test_receiver_device, 'ALERT', 'Trouble', 0, 'R')
        with contextlib.redirect_stdout(io.StringIO()) as output:
            test_event.log()
        self.assertEqual(output.getvalue(), "@0: #3 RECEIVED ALERT FROM #2: Trouble\n")

    def setUp(self) -> None:
        self.device_1 = Device(1, 10)
        self.device_2 = Device(2, 10)
        self.device_3 = Device(3, 10)
        self.device_2.add_recipient(self.device_3, 500)
        self.event_queue = []

    def test_execute_receive_phase(self) -> None:
        event = Event(self.device_1, self.device_2, "ALERT", "Test Alert", 5, 'R')

        with contextlib.redirect_stdout(io.StringIO()) as output:
            event.execute(self.event_queue)

        expected_log = ("@5: #2 RECEIVED ALERT FROM #1: Test Alert\n"
                       "@5: #2 SENT ALERT TO #3: Test Alert\n")

        self.assertEqual(output.getvalue(), expected_log)
        self.assertEqual(len(self.event_queue), 0)



    def test_execute_send_phase(self) -> None:
        event = Event(self.device_1, self.device_2, 'ALERT', 'Test Alert', 5, 'S')
        with contextlib.redirect_stdout(io.StringIO()) as output:
            event.execute(self.event_queue)

        expected_log = "@5: #2 SENT ALERT TO #3: Test Alert\n"
        self.assertEqual(output.getvalue(), expected_log)
        self.assertEqual(len(self.event_queue), 0)




if __name__ == '__main__':
    unittest.main()