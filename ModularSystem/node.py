from utils.misc_utils import dataname_to_index
from Modules.util_modules import *


class Node:
    def __init__(self, module_name, module_object, input_nodes=None, output_nodes=None):

        self.input_nodes = input_nodes if input_nodes is not None else ([], [], [])
        self.output_nodes = output_nodes if output_nodes is not None else ([], [], [])

        # self.input_mixer = Mixer()
        # self.received_all_inputs = False
        # self.sent_all_outputs = False
        self.ready_to_send_outputs = False
        self.ready_to_receive_inputs = False

        self.module_name = module_name
        self.module = module_object

    def is_output_node(self):
        return False

    def get_module(self):
        return self.module

    def add_output_node(self, node, output_type):
        if output_type not in ['video', 'audio', 'modulation']:
            return False
        idx = dataname_to_index(output_type)
        if node.module_name not in self.output_nodes[idx]:
            self.output_nodes[idx].append(node)
        return 0

    def remove_output_node(self, node, output_type):
        if output_type not in ['video', 'audio', 'modulation']:
            return -1
        idx = dataname_to_index(output_type)
        try:
            self.output_nodes[idx].remove(node)
            return 0
        except ValueError:
            return 0

    def add_input_node(self, node, input_type):
        if input_type not in ['video', 'audio', 'modulation']:
            return False
        idx = dataname_to_index(input_type)
        if node.module_name not in self.input_nodes[idx]:
            self.input_nodes[idx].append(node)
        return 0

    def remove_input_node(self, node, input_type):
        if input_type not in ['video', 'audio', 'modulation']:
            return -1
        idx = dataname_to_index(input_type)
        try:
            self.input_nodes[idx].remove(node)
            return 0
        except ValueError:
            return 0

    def send_all_outputs(self):
        if self.module.emits_video:
            out_nodes = self.output_nodes[dataname_to_index('video')]
            for out_node in out_nodes:
                out_node.module.video_input_buffer = self.module.video_output_buffer
        if self.module.emits_audio:
            out_nodes = self.output_nodes[dataname_to_index('audio')]
            for out_node in out_nodes:
                out_node.module.video_input_buffer = self.module.video_output_buffer
        if self.module.emits_modulation:
            out_nodes = self.output_nodes[dataname_to_index('modulation')]
            for out_node in out_nodes:
                out_node.module.video_input_buffer = self.module.video_output_buffer
        return True

    def get_inputs(self):
        if self.module.accepts_video:
            in_nodes = self.input_nodes[dataname_to_index('video')]
            for i, node in enumerate(in_nodes):
                if i == 0:
                    self.module.video_input_buffer = node.module.video_output_buffer // len(in_nodes)
                else:
                    self.module.video_input_buffer = (node.module.video_output_buffer // len(in_nodes))

        if self.module.accepts_audio:
            in_nodes = self.input_nodes[dataname_to_index('audio')]
            for node in in_nodes:
                self.module.audio_input_buffer = node.module.audio_output_buffer
        if self.module.accepts_modulation:
            in_nodes = self.input_nodes[dataname_to_index('modulation')]
            for node in in_nodes:
                self.module.modulation_input_buffer = node.module.modulation_output_buffer

    def tick(self):
        if self.ready_to_receive_inputs and not self.ready_to_send_outputs:
            self.get_inputs()
            self.module.tick()
            self.ready_to_send_outputs = True


class OutputNode(Node):
    def __init__(self):
        super(OutputNode, self).__init__(self, 'OUT', IdentityModule())

    def is_output_node(self):
        return True


class Mixer:
    def __init__(self):
        self.mix_ratios = None

    def set_mix_ratios(self, m):
        self.mix_ratios = m

    def mix(self, input_nodes):
        pass

