from event import Event

class Device:
    simulation_length = 0
    def __init__(self, device_id, simulation_length):
        self._device_id = device_id
        self._recipients = []
        self._cancelled_descriptions = []
        Device.simulation_length = simulation_length

    def get_device_id(self) -> int:
        """Gets device id"""
        return self._device_id

    def get_recipients(self) -> list[tuple]:
        """Gets recipients"""
        return self._recipients

    def get_cancelled_descriptions(self) -> list[tuple]:
        """Gets cancelled descriptions"""
        return self._cancelled_descriptions

    def add_recipient(self, receiver: 'Device', delay: int) -> None:
        """Adds recipients in tuple with receiver device and delay"""
        self._recipients.append((receiver, delay))

    def send_message(self, event: 'Event') -> list[Event]:
        """Takes event and sends message to the receiver devices recipients"""
        receiving_events = []

        for recipient, delay in self.get_recipients():
            new_event = Event(self, recipient, event.get_event_type(), event.get_description(),
                              event.get_time(), 'S')
            new_event.log()

            receiving_event = recipient.receive_message(new_event, delay)
            if receiving_event:
                receiving_events.append(receiving_event)
        return receiving_events

    def receive_message(self, event: 'Event', delay: int) -> Event or None:
        """Receives message based on the previous event and the delay"""
        if event.get_time() + delay < Device.simulation_length:
            new_event = Event(event.get_sender(), self, event.get_event_type(), event.get_description(),
                              event.get_time() + delay, 'R')
            return new_event
        return None

    def process_events(self, event: 'Event', event_queue: list) -> None:
        """Processes events and calls send and receive message functions"""
        if event.get_time() >= Device.simulation_length:
            return

        if event.get_event_type() == "CANCELLATION":
            if event.get_description() not in [desc for desc, _ in self.get_cancelled_descriptions()]:
                receiving_events = self.send_message(event)
                for temp_event in receiving_events:
                    event_queue.append(temp_event)
                self.get_cancelled_descriptions().append((event.get_description(), event.get_time()))
            return

        for description, cancel_time in self.get_cancelled_descriptions():
            if event.get_description() == description and event.get_time() >= cancel_time + 1:
                return

        receiving_events = self.send_message(event)
        for temp_event in receiving_events:
            event_queue.append(temp_event)