import unittest
from device import Device
from event import Event
import io
import contextlib



class DeviceClassTest(unittest.TestCase):
    def test_device_id(self) -> None:
        test_device = Device(1, 999)
        self.assertEqual(test_device.get_device_id(), 1)

    def test_device_simulation_length(self) -> None:
        test_device = Device(7, 999)
        self.assertEqual(Device.simulation_length, 999)

    def test_one_recipient_add(self) -> None:
        test_device = Device(3, 999)
        receiver_device = Device(2, 999)
        delay = 550
        test_device.add_recipient(receiver_device, delay)
        self.assertEqual(test_device.get_recipients(), [(receiver_device, delay)])

    def test_multiple_recipients_add(self) -> None:
        test_device = Device(2, 999)
        receiver_device_one = Device(3, 999)
        receiver_device_two = Device(4, 999)
        receiver_device_three = Device(5, 999)
        test_device.add_recipient(receiver_device_one, 450)
        test_device.add_recipient(receiver_device_two, 550)
        test_device.add_recipient(receiver_device_three, 650)
        self.assertEqual(test_device.get_recipients(), [(receiver_device_one, 450), (receiver_device_two, 550), (receiver_device_three, 650)])

    def test_receive_message(self) -> None:
        sender_device = Device(1, 999)
        test_device = Device(2, 999)
        delay = 550

        test_event = Event(sender_device, test_device, 'ALERT', 'Oh no', 0, 'S')

        received_event = test_device.receive_message(test_event, delay)
        expected_event = Event(sender_device, test_device, 'ALERT', 'Oh no', 550, 'R')

        self.assertEqual(received_event.get_sender().get_device_id(), expected_event.get_sender().get_device_id())
        self.assertEqual(received_event.get_receiver().get_device_id(), expected_event.get_receiver().get_device_id())
        self.assertEqual(received_event.get_event_type(), expected_event.get_event_type())
        self.assertEqual(received_event.get_description(), expected_event.get_description())
        self.assertEqual(received_event.get_time(), expected_event.get_time())
        self.assertEqual(received_event.get_phase(), expected_event.get_phase())


    def test_send_message(self) -> None:
        origin_device = Device(1, 999)
        receiver_device = Device(2, 999)
        other_receiver_device = Device(3, 999)
        origin_device.add_recipient(receiver_device, 550)
        origin_device.add_recipient(other_receiver_device, 800)
        test_event = Event(None, origin_device, 'ALERT', 'Uh oh', 0, 'S')


        with contextlib.redirect_stdout(io.StringIO()) as output:
            receiving_events_list = origin_device.send_message(test_event)
        self.assertEqual(output.getvalue(), "@0: #1 SENT ALERT TO #2: Uh oh\n"
                                            "@0: #1 SENT ALERT TO #3: Uh oh\n")


        first_event = receiving_events_list[0]
        second_event = receiving_events_list[1]

        expected_first_event = Event(origin_device, receiver_device, 'ALERT', 'Uh oh', 550, 'R')
        expected_second_event = Event(origin_device, other_receiver_device, 'ALERT', 'Uh oh', 800, 'R')

        self.assertEqual(first_event.get_sender().get_device_id(), expected_first_event.get_sender().get_device_id())
        self.assertEqual(first_event.get_receiver().get_device_id(), expected_first_event.get_receiver().get_device_id())
        self.assertEqual(first_event.get_event_type(), expected_first_event.get_event_type())
        self.assertEqual(first_event.get_description(), expected_first_event.get_description())
        self.assertEqual(first_event.get_time(), expected_first_event.get_time())
        self.assertEqual(first_event.get_phase(), expected_first_event.get_phase())

        self.assertEqual(second_event.get_sender().get_device_id(), expected_second_event.get_sender().get_device_id())
        self.assertEqual(second_event.get_receiver().get_device_id(), expected_second_event.get_receiver().get_device_id())
        self.assertEqual(second_event.get_event_type(), expected_second_event.get_event_type())
        self.assertEqual(second_event.get_description(), expected_second_event.get_description())
        self.assertEqual(second_event.get_time(), expected_second_event.get_time())
        self.assertEqual(second_event.get_phase(), expected_second_event.get_phase())

    def setUp(self) -> None:
        self.device1 = Device(1, 10)
        self.device2 = Device(2, 10)
        self.device3 = Device(3, 10)
        self.device1.add_recipient(self.device2, 2)
        self.device2.add_recipient(self.device3, 3)

    def test_process_normal_event(self) -> None:
        event_queue = []
        event = Event(self.device1, self.device1, "ALERT", "Test Event", 1, 'S')


        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.device1.process_events(event, event_queue)
        self.assertEqual(output.getvalue(), "@1: #1 SENT ALERT TO #2: Test Event\n")

        self.assertEqual(len(event_queue), 1)
        self.assertEqual(event_queue[0].get_sender(), self.device1)
        self.assertEqual(event_queue[0].get_receiver(), self.device2)
        self.assertEqual(event_queue[0].get_event_type(), "ALERT")
        self.assertEqual(event_queue[0].get_description(), "Test Event")
        self.assertEqual(event_queue[0].get_time(), 3)
        self.assertEqual(event_queue[0].get_phase(), 'R')

    def test_process_cancellation_event(self) -> None:
        event_queue = []
        cancellation_event = Event(self.device1, self.device1, "CANCELLATION", "Cancel Task", 2,
                                   'S')

        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.device1.process_events(cancellation_event, event_queue)
        self.assertEqual(output.getvalue(), "@2: #1 SENT CANCELLATION TO #2: Cancel Task\n")

        self.assertEqual(len(event_queue), 1)
        self.assertEqual(event_queue[0].get_event_type(), "CANCELLATION")
        self.assertEqual(event_queue[0].get_description(), "Cancel Task")
        self.assertEqual(event_queue[0].get_sender(), self.device1)
        self.assertEqual(event_queue[0].get_receiver(), self.device2)

        self.assertIn(("Cancel Task", 2), self.device1.get_cancelled_descriptions())

    def test_event_ignored_after_cancellation(self) -> None:
        event_queue = []
        cancellation_event = Event(self.device1, self.device1, "CANCELLATION", "Cancel Task", 2,
                                   'S')

        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.device1.process_events(cancellation_event, event_queue)
        self.assertEqual(output.getvalue(), "@2: #1 SENT CANCELLATION TO #2: Cancel Task\n")


        event = Event(self.device1, self.device1, "ALERT", "Cancel Task", 4, 'S')
        self.device1.process_events(event, event_queue)

        self.assertEqual(len(event_queue), 1)

    def test_event_outside_simulation_length(self) -> None:
        event_queue = []
        event = Event(self.device1, self.device1, "ALERT", "Late Event", 9, 'S')

        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(self.device1.process_events(event, event_queue), None)
        self.assertEqual(output.getvalue(), "@9: #1 SENT ALERT TO #2: Late Event\n")
        self.assertEqual(len(event_queue), 0)

    def test_event_at_simulation_length(self) -> None:
        event_queue = []
        event = Event(self.device1, self.device1, "ALERT", "Edge Case Event", 10, 'S')

        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.device1.process_events(event, event_queue)

        # Since event time equals simulation length, it should be ignored
        self.assertEqual(len(event_queue), 0)
        self.assertEqual(output.getvalue(), "")


if __name__ == '__main__':
    unittest.main()
