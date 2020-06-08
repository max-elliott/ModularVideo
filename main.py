from imageio import get_reader, get_writer
from matplotlib import pyplot as plt
from imageio_ffmpeg import read_frames, write_frames
from Modules.video_modules import *
from ModularSystem.modular_instrument import ModuleNet, Instrument
import numpy as np
from timeit import default_timer as timer


def main():
    home = '/Users/Max/'
    filename = home + '/Documents/videos/daily_dose1.mp4'
    out_filename = home + '/Documents/videos/daily_dose1_edited.mp4'

    reader = get_reader(filename)
    meta = reader.get_meta_data()

    writer = write_frames(out_filename, meta['size'], fps=meta['fps'])
    writer.send(None)

    start_offset = 4170

    looper = Looper(meta)
    looper.set_video(reader)
    looper.set_offset(start_offset)
    looper.set_loop_length(500)
    looper.set_frame_interval(5)
    reducer = BitReducer(meta)
    sharpen = Sharpener(meta)
    delay = VideoDelay(meta)

    net = ModuleNet()
    net.add_module(looper)
    # net.add_module(sharpen, input_names=(['Looper0'], [], []))
    # net.add_module(reducer, input_names=(['Looper0'], [], []), output_names=([], [], []))
    net.add_module(delay, input_names=(['Looper0'], [], []), output_names=(['OUT'], [], []))

    # net.nodes['BitReducer0'].module.set_num_bits(2)
    # net.nodes['Sharpener0'].module.set_strength(7)

    sharpen_max_strength = 20
    sharpen_min_strength = 10
    sharpen_delta = (sharpen_max_strength - sharpen_min_strength) / 2
    angular_period = 2*np.pi/30

    instrument = Instrument()
    instrument.net = net

    total_frames = 300

    start_time = timer()

    for i in range(total_frames):
        # net.nodes['Sharpener0'].module.set_strength(sharpen_min_strength + sharpen_delta + sharpen_delta * np.sin(angular_period * i))
        #
        # net.nodes['Looper0'].tick()
        # net.nodes['Sharpener0'].tick()
        # net.nodes['BitReducer0'].tick()
        # instrument.reset_flags()
        # print(net.nodes['Looper0'].module.current_frame)

        video_frame = instrument.tick()
        # frame = net.nodes['BitReducer0'].module.video_output_buffer
        writer.send(video_frame)
    #     # print(looper.current_frame)

    end_time = timer()

    reader.close()
    writer.close()

    print(f"Time taken to run {total_frames} frames: {end_time - start_time}s.")


def test():

    home = '/Users/Max/'
    filename = home + '/Documents/videos/daily_dose1.mp4'
    out_filename = home + '/Documents/videos/daily_dose1_edited.mp4'

    reader = get_reader(filename)
    meta = reader.get_meta_data()


if __name__ == '__main__':
    main()
    # test()
