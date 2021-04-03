# ModularVideo
Modular video processing system inspired by modular synthesisers.

Each module has 3 different inputs and outputs: video, audio, and modulation (equivalent to control voltage in modular synths).
Modules can process input video/audio/modulations or generate new data entirely, which is then passed to the outputs.
Modules can be connected to any number of other modules so that module input/output signals feed into one another.

Modules are defined as a node in a graph, which is held and maintained by an intstrument class, that will run the modules globally.

This implementation is in its early stages, with most of the basic infrastructure set up. More modules need to be devised and implemented.
