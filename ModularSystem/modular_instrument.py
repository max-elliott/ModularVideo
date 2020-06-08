from ModularSystem.node import *
from Modules.util_modules import IdentityModule

class ModuleNet:
    def __init__(self):
        self.nodes = {}

        self.add_module(IdentityModule())
        self.nodes['OUT'] = self.nodes.pop('IdentityModule0')
        # self.nodes['OUT'] = OutputNode()

    def __iter__(self):
        # print(self.nodes.values())
        return iter(self.nodes.values())

    def add_module(self, module, input_names=None, output_names=None):
        """
        input_names =
        BUG: If name in input names doesn't exist, module will be made, but connections won't. Will still work, but should
        be caught.
        """

        output_names = output_names if output_names is not None else ([], [], [])
        input_names = input_names if input_names is not None else ([], [], [])

        module_class_name = module.__class__.__name__
        module_name = ''
        found_unique_name = False
        i = 0
        while not found_unique_name:
            found_unique_name = True
            module_name = module_class_name + str(i)
            for node_name in self.nodes.keys():
                if module_name == node_name:
                    found_unique_name = False
            i += 1

        self.nodes[module_name] = Node(module_name, module)

        vid_out, audio_out, mod_out = output_names
        for other_module_name in vid_out:
            self.add_connection(module_name, other_module_name, 'video')
        for other_module_name in audio_out:
            self.add_connection(module_name, other_module_name, 'audio')
        for other_module_name in mod_out:
            self.add_connection(module_name, other_module_name, 'modulation')

        vid_in, audio_in, mod_in = input_names

        for other_module_name in vid_in:
            self.add_connection(other_module_name, module_name, 'video')
        for other_module_name in audio_in:
            self.add_connection(other_module_name, module_name, 'audio')
        for other_module_name in mod_in:
            self.add_connection(other_module_name, module_name, 'modulation')

        return 0

    def add_connection(self, node_name1, node_name2, connection_type):
        self.nodes[node_name1].add_output_node(self.nodes[node_name2], connection_type)
        self.nodes[node_name2].add_input_node(self.nodes[node_name1], connection_type)

    def get_output(self):
        return self.nodes['OUT'].module.video_output_buffer


class Instrument:
    def __init__(self):
        self.video_input_stream = None
        self.audio_input_stream = None
        self.video_output_buffer = None
        self.audio_output_buffer = None

        self.net = ModuleNet()

    def reset_flags(self):
        for n in self.net:
            n.ready_to_send_outputs = False
            n.ready_to_receive_inputs = n.module.is_generator()

    def tick(self):
        '''
        Execute full frame pass of system.
        1) Read in input frame
        2) Process modules
        3) Write frame to output buffers

        algorithm:
        i) Check if all nodes have sent_all_outputs = True: return
        ii) else:
            for each node: if all parents have sent_all_outputs, set received_all_inputs = True
        ii)
            for each node: if received_all_inputs, tick, and send_all_outputs
        '''
        self.reset_flags()

        finished = False
        while not finished:
            finished = True
            for n in self.net:
                if not n.ready_to_send_outputs:
                    finished = False
                    # break

            for n in self.net:
                received_all = True
                vid_in, audio_in, mod_in = n.input_nodes
                for m in vid_in + audio_in + mod_in:
                    if not m.ready_to_send_outputs:
                        received_all = False
                n.ready_to_receive_inputs = received_all

            for n in self.net:
                if n.ready_to_receive_inputs:
                    n.tick()

        self.video_output_buffer = self.net.get_output()
        return self.video_output_buffer




