from pathlib import Path
from device import Device
from event import Event

def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())

def parse_input_file(file_path: Path) -> (int, list[Device], list[dict]):
    """Parses the file and returns simulation length, list of devices, and actions"""
    try:
        with open(file_path, 'r') as file:
            file_contents = file.readlines()
    except:
        print('FILE NOT FOUND')
        quit()

    important_lines = []
    for line in file_contents:
        if line and line[0] not in ['', ' ', '\n', '#']:
            important_lines.append(line.strip())

    simulation_length = 0
    device_list = []
    propagation_rules = []
    event_list = []

    for line in important_lines:
        if line.startswith('LENGTH'):
            simulation_length = int(line[7:])
        elif line.startswith('DEVICE'):
            device_list.append(int(line[7:]))
        elif line.startswith('PROPAGATE'):
            sender, receiver, delay = line[10:].split()
            propagation_rules.append({
                'sender': int(sender),
                'receiver': int(receiver),
                'delay': int(delay)
            })
        elif line.startswith('ALERT'):
            beginning_device, description, time = line[6:].split()
            event_list.append((int(beginning_device), description, int(time), 'ALERT'))

        elif line.startswith('CANCEL'):
            beginning_device, description, time = line[7:].split()
            event_list.append((int(beginning_device), description, int(time), 'CANCELLATION'))


    #Creates a list of Device objects and adds corresponding recipient devices
    device_with_classes_list = []

    for device in device_list:
        device_with_classes_list.append(Device(device, simulation_length))

    for rule in propagation_rules:
        for device in device_with_classes_list:
            if rule['sender'] == device.get_device_id():
                for other_device in device_with_classes_list:
                    if other_device.get_device_id() == rule['receiver']:
                        device.add_recipient(other_device, rule['delay'])

    #Creates a list of Event objects
    event_with_classes_list = []
    for device in device_with_classes_list:
        for event in event_list:
            if event[0] == device.get_device_id():
                start_event = Event(None, device, event[3], event[1], event[2], 'S')
                event_with_classes_list.append(start_event)

    return simulation_length, device_with_classes_list, event_with_classes_list

def run_simulation(simulation_length, event_list) -> None:
    """Runs simulation using a while loop to go until it ends"""
    event_queue = sorted(event_list, key=lambda e: e.get_time())

    while event_queue:
        event_queue.sort(key=lambda e: (e.get_time(), 0 if e.get_event_type() == 'ALERT' else 1))
        current_event = event_queue.pop(0)

        if current_event.get_time() >= simulation_length:
            break
        current_event.execute(event_queue)

    print(f'@{simulation_length}: END')

def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()
    simulation_length, device_list, event_list = parse_input_file(input_file_path)
    run_simulation(simulation_length, event_list)

if __name__ == '__main__':
    main()
