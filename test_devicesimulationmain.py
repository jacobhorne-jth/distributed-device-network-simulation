import unittest
from device import Device
from event import Event
import tempfile
from devicesimulationmain import parse_input_file, run_simulation
from pathlib import Path
import io
import contextlib


class SimulationTest(unittest.TestCase):
    def test_parse_input_file_alert(self) -> None:
        with tempfile.NamedTemporaryFile(mode = 'w', delete_on_close = False) as temp:
            temp.write(
                '# sample_input.txt\n'
                '# example will occur before the simulation ends.\n'
                'LENGTH 600\n'
                'DEVICE 1\n'
                'DEVICE 2\n'
                'DEVICE 3\n'
                'PROPAGATE 1 2 750\n'
                'PROPAGATE 2 3 1250\n'
                'PROPAGATE 3 1 500\n'
                'ALERT 1 Trouble 0\n'
            )
            temp.flush()

            simulation_length, parsed_devices, parsed_events = parse_input_file(Path(temp.name))

            device_list = [
                Device(1, 600),
                Device(2, 600),
                Device(3, 600)
            ]

            device_list[0].add_recipient(2, 750)
            device_list[1].add_recipient(3, 1250)
            device_list[2].add_recipient(1, 500)

            event_list = [Event(None, device_list[0], 'ALERT', 'Trouble', 0, 'S')]

            self.assertEqual(simulation_length, 600)

            for i in range(len(parsed_devices)):
                self.assertEqual(device_list[i].get_device_id(), parsed_devices[i].get_device_id())

            for i in range(len(parsed_events)):
                self.assertEqual(event_list[i].get_receiver().get_device_id(),
                                parsed_events[i].get_receiver().get_device_id())
                self.assertEqual(event_list[i].get_event_type(), parsed_events[i].get_event_type())
                self.assertEqual(event_list[i].get_description(), parsed_events[i].get_description())
                self.assertEqual(event_list[i].get_time(), parsed_events[i].get_time())
                self.assertEqual(event_list[i].get_phase(), parsed_events[i].get_phase())


    def test_parse_input_file_cancel(self) -> None:
        with tempfile.NamedTemporaryFile(mode = 'w', delete_on_close = False) as temp:
            temp.write(
                '# sample_input.txt\n'
                '# example will occur before the simulation ends.\n'
                'LENGTH 600\n'
                'DEVICE 1\n'
                'DEVICE 2\n'
                'DEVICE 3\n'
                'PROPAGATE 1 2 750\n'
                'PROPAGATE 2 3 1250\n'
                'PROPAGATE 3 1 500\n'
                'CANCEL 1 Trouble 0\n'
            )
            temp.flush()

            simulation_length, parsed_devices, parsed_events = parse_input_file(Path(temp.name))

            device_list = [
                Device(1, 600),
                Device(2, 600),
                Device(3, 600)
            ]

            device_list[0].add_recipient(2, 750)
            device_list[1].add_recipient(3, 1250)
            device_list[2].add_recipient(1, 500)

            event_list = [Event(None, device_list[0], 'CANCELLATION', 'Trouble', 0, 'S')]

            self.assertEqual(simulation_length, 600)

            for i in range(len(parsed_devices)):
                self.assertEqual(device_list[i].get_device_id(), parsed_devices[i].get_device_id())

            for i in range(len(parsed_events)):
                self.assertEqual(event_list[i].get_receiver().get_device_id(),
                                parsed_events[i].get_receiver().get_device_id())
                self.assertEqual(event_list[i].get_event_type(), parsed_events[i].get_event_type())
                self.assertEqual(event_list[i].get_description(), parsed_events[i].get_description())
                self.assertEqual(event_list[i].get_time(), parsed_events[i].get_time())
                self.assertEqual(event_list[i].get_phase(), parsed_events[i].get_phase())


    def test_file_not_found(self) -> None:
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                parse_input_file(Path("non_existent_file.txt"))
            self.assertEqual(output.getvalue(), "FILE NOT FOUND\n")

    def test_run_simulation(self):
        device1 = Device(1, 500)
        device2 = Device(2, 500)
        device3 = Device(3, 500)

        device1.add_recipient(device2, 100)
        device2.add_recipient(device3, 200)

        event1 = Event(None, device1, 'ALERT', 'Danger', 0, 'S')
        event2 = Event(None, device2, 'CANCELLATION', 'Danger', 250, 'S')

        with contextlib.redirect_stdout(io.StringIO()) as output:
            run_simulation(500, [event1, event2])
            output_value = output.getvalue().strip()

        self.assertIn("@500: END", output_value)

    def test_event_after_simulation_length(self):
        device1 = Device(1, 300)
        device2 = Device(2, 300)

        device1.add_recipient(device2, 100)

        event1 = Event(None, device1, 'ALERT', 'Late Alert', 350, 'S')

        with contextlib.redirect_stdout(io.StringIO()) as output:
            run_simulation(300, [event1])
            output_value = output.getvalue().strip()

        self.assertIn("@300: END", output_value)
        self.assertNotIn("Late Alert", output_value)

if __name__ == '__main__':
    unittest.main()

