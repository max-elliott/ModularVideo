from Modules.base_classes import *


class Mixer(Module):
    def __init__(self):
        super(Mixer, self).__init__((True, True, True), (True, True, True))


class IdentityModule(Module):
    def __init__(self):
        super(IdentityModule, self).__init__((True, True, True), (True, True, True))

        self.video_input_buffer = None
        self.audio_input_buffer = None
        self.modulation_input_buffer = None
        self.video_output_buffer = None
        self.audio_output_buffer = None
        self.modulation_output_buffer = None

    def tick(self):
        self.video_output_buffer = self.video_input_buffer
        self.audio_output_buffer = self.audio_input_buffer
        self.modulation_output_buffer = self.modulation_input_buffer
