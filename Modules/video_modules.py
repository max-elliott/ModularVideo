from Modules.base_classes import *
# from scipy import ndimage
from skimage.filters import gaussian
import numpy as np


class Looper(VideoModule):
    def __init__(self, video_metadata):
        super(Looper, self).__init__(video_metadata)
        # super(Looper, self).__init__((True, False, False), (True, False, False))
        self.current_frame = 0
        self.loop_length = 50  # num frames to loop
        self.frame_interval = 1
        self.input_stream = None
        self.output_stream = None
        self.start_offset = 0
        self.is_looping = True

        self.loop_buffer = None

    def is_generator(self):
        return self.is_looping

    def set_loop_buffer(self):
        pass

    def set_loop_length(self, num_frames):
        self.loop_length = num_frames

    def reset_loop(self):
        self.current_frame = 0

    def set_video(self, video_stream):
        self.input_stream = video_stream
        self.start_offset = 0

    def set_offset(self, offset):
        self.start_offset = offset

    def set_frame_interval(self, i):
        self.frame_interval = i

    def tick(self):
        self.video_output_buffer = self.input_stream.get_data(self.start_offset + (self.current_frame * self.frame_interval))
        self.current_frame = (self.current_frame + 1) % self.loop_length


class BitReducer(ModulatedVideoModule):
    def __init__(self, video_metadata):
        super(BitReducer, self).__init__(video_metadata)

        self.num_bits = 1

    def set_num_bits(self, num_bits):
        self.num_bits = int(num_bits)

    def reduce(self, frame):
        if self.active_planes == [0, 1, 2]:
            return frame << self.num_bits
        else:
            print(f'{self.__class__}: Dynamic plane processing not implemented yet')
            for plane in self.active_planes:
                pass
            return frame << self.num_bits

    def tick(self):
        self.video_output_buffer = self.reduce(self.video_input_buffer)


class Sharpener(ModulatedVideoModule):
    def __init__(self, video_metadata):
        super(Sharpener, self).__init__(video_metadata)

        self.strength = 5
        self.alpha = 30

    def set_strength(self, st):
        self.strength = st

    def filter(self, frame):
        # return self.alpha * frame - (1 - self.alpha) * ndimage.gaussian_filter(frame, self.strength)
        return gaussian(frame, sigma=self.strength, multichannel=True, preserve_range=True).astype('uint8')

    def tick(self):
        self.video_output_buffer = self.filter(self.video_input_buffer)


class VideoDelay(ModulatedVideoModule):
    def __init__(self, video_metadata):
        super(VideoDelay, self).__init__(video_metadata)

        self.max_length = 15  # in num frames
        self.feedback = 90
        self.current_frame = 0

        self.delay_buffer = np.zeros((self.max_length, self.height, self.width, self.num_channels), dtype=np.uint32)

    def reset_delay_buffer(self):
        self.delay_buffer = np.zeros((self.max_length, self.height, self.width, self.num_channels), dtype=np.uint32)

    def reset(self):
        self.reset_delay_buffer()
        self.current_frame = 0

    def tick(self):
        tmp_input = self.video_input_buffer.astype('uint32') + self.delay_buffer[self.current_frame, :, :, :] # 65535 255
        if self.enabled:
            self.delay_buffer[self.current_frame, :, :, :] = tmp_input * self.feedback / 100
        else:
            self.delay_buffer[self.current_frame, :, :, :] = self.delay_buffer[self.current_frame, :, :, :] * self.feedback / 100

        tmp_input = (tmp_input * 255) // np.max(tmp_input)
        self.video_output_buffer = tmp_input.astype(self.pix_fmt)
        self.current_frame = (self.current_frame + 1) % self.max_length

        pass

