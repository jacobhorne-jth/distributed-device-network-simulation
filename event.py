class Event:
    def __init__(self, sender: 'Device', receiver: 'Device', event_type: str, description: str, time: int, phase: str):
        self._sender = sender
        self._receiver = receiver
        self._event_type = event_type
        self._description = description
        self._time = time
        self._phase = phase

    def get_sender(self) -> 'Device':
        """Gets sender device"""
        return self._sender

    def get_receiver(self) -> 'Device':
        """Gets receiver device"""
        return self._receiver

    def get_event_type(self) -> str:
        """Gets event type"""
        return self._event_type

    def get_description(self) -> str:
        """Gets description"""
        return self._description

    def get_time(self) -> int:
        """Gets time"""
        return self._time

    def get_phase(self) -> str:
        """Gets phase"""
        return self._phase

    def log(self) -> None:
        """Logs devices by printing them according to the correct format"""
        if self.get_phase() == 'R':
            print(f'@{self.get_time()}: #{self.get_receiver().get_device_id()} RECEIVED {self.get_event_type()} FROM #{self.get_sender().get_device_id()}: {self.get_description()}')
        elif self.get_phase() == 'S':
            print(f'@{self.get_time()}: #{self.get_sender().get_device_id()} SENT {self.get_event_type()} TO #{self.get_receiver().get_device_id()}: {self.get_description()}')

    def execute(self, event_queue: list['Event']) -> None:
        """Executes for the given event_queue by logging or processing"""
        if self.get_phase() == 'R':
            self.log()
        if self.get_receiver():
            self.get_receiver().process_events(self, event_queue)