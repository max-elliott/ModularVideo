import numpy as np


class Module:
    def __init__(self, inputs, outputs):
        self.accepts_video, self.accepts_audio, self.accepts_modulation = inputs
        self.emits_video, self.emits_audio, self.emits_modulation = outputs

    def is_generator(self):
        return False

    def tick(self):
        raise NotImplementedError()


class VideoModule(Module):
    def __init__(self, video_metadata):
        super(VideoModule, self).__init__((True, False, False), (True, False, False))
        self.metadata = video_metadata
        self.width = video_metadata['source_size'][0]
        self.height = video_metadata['source_size'][1]
        self.pix_fmt = np.uint16 if 'yuv420p10' in video_metadata['pix_fmt'] else np.uint8  # needs doing better another time
        self.num_channels = 3 if 'yuv' in video_metadata['pix_fmt'] else 1  # needs doing better another time

        self.video_input_buffer = None
        self.video_output_buffer = None
        self.active_planes = [0, 1, 2]

    def set_active_planes(self, planes):
        for p in planes:
            if p not in [0, 1, 2]:
                raise ValueError
        self.active_planes = planes

    def tick(self):
        raise NotImplementedError()


class ModulatedVideoModule(Module):
    def __init__(self, video_metadata):
        super(ModulatedVideoModule, self).__init__((True, False, True), (True, False, False))
        self.metadata = video_metadata
        self.width = video_metadata['source_size'][0]
        self.height = video_metadata['source_size'][1]
        self.pix_fmt = np.uint16 if 'yuv420p10' in video_metadata['pix_fmt'] else np.uint8  # needs doing better another time
        self.num_channels = 3 if 'yuv' in video_metadata['pix_fmt'] else 1  # needs doing better another time

        self.video_input_buffer = None
        self.video_output_buffer = None
        self.active_planes = [0, 1, 2]

    def set_active_planes(self, planes):
        for p in planes:
            if p not in [0, 1, 2]:
                raise ValueError
        self.active_planes = planes

    def tick(self):
        raise NotImplementedError()
