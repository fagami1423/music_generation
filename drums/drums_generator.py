'''
The code generates a drum track MIDI file and a plot of its corresponding drum roll.
The code sets up a drum track and uses Magenta to generate a new piece of music based on that drum track.
It then saves the generated music as a MIDI file, which can be played using a MIDI player. The code also
generates a visual representation of the generated music, which can be helpful for understanding what the computer created.
'''

import os
'''
This line imports the "magenta.music" module and renames it to "mm". The "magenta.music" module provides 
functions for reading, writing, and manipulating MIDI files.
'''
import magenta.music as mm
'''
This line imports a module called "sequence_generator_bundle" from the "magenta.models.shared" module. 
The "sequence_generator_bundle" module provides a way to read a bundle file
'''
from magenta.models.shared import sequence_generator_bundle
# mm.notebook_utils.download_bundle("drum_kit_rnn.mag", "bundles")
'''
This line imports a module called "drums_rnn_sequence_generator" from the "magenta.models.drums_rnn" module.
The "drums_rnn_sequence_generator" module provides a way to generate drum sequences using a pre-trained RNN model.
'''
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.music import constants



#This line reads the "drum_kit_rnn.mag" bundle file from the "bundles" directory and stores it in a variable called "bundle".
bundle = sequence_generator_bundle.read_bundle_file(os.path.join("bundles", "drum_kit_rnn.mag"))

#This line creates a map of all the available generators.
generator_map = drums_rnn_sequence_generator.get_generator_map()

#This line creates an instance of the "drum_kit" generator from the "generator_map".
generator = generator_map["drum_kit"](checkpoint=None, bundle=bundle)

#This line initializes the generator.
generator.initialize()

# This line sets the tempo (in beats per minute) to 120.
qpm = 120

#This line calculates the number of seconds per step in the drum sequence.
seconds_per_step = 60.0 / qpm / generator.steps_per_quarter

#This line sets the number of steps per bar to the default value specified in the "constants" module.
num_steps_per_bar = constants.DEFAULT_STEPS_PER_BAR

#This line calculates the number of seconds per bar in the drum sequence.
seconds_per_bar = num_steps_per_bar * seconds_per_step

print("seconds per step: ", seconds_per_step)
print("seconds per bar: ", seconds_per_bar)

# This line creates a "DrumTrack" object called "primer_drums", which is a sequence of drum sounds.
primer_drums = mm.DrumTrack(
    [frozenset(pitches) for pitches in
     [(38, 51), (), (36,), (),
      (38, 44, 51), (), (36,), (),
      (), (), (38,), (),
      (38, 44), (), (36, 51), (), ]])
'''
This line converts the "primer_drums" object into a "sequence" object. A sequence is like a musical score,
it contains information about the timing, pitch, and duration of musical notes. By converting the "primer_drums" 
object into a sequence, we can then feed it into the machine learning model to generate new music based on the 
information contained in the sequence. The "qpm" argument stands for "quater-notes per minute" and it sets the 
tempo or speed of the music in the sequence.
'''
primer_sequence = primer_drums.to_sequence(qpm=qpm)
'''
Here, we are setting the start and end time for the primer_sequence we generated before.
primer_start_time is set to 0, which means the drum pattern will start playing from the beginning. 
primer_end_time is set to primer_start_time plus seconds_per_bar, which means the drum pattern will 
end playing after one bar.
'''
primer_start_time = 0
primer_end_time = primer_start_time + seconds_per_bar

'''
Here, we are setting the start and end time for the newly generated music. num_bars is set to 3,
which means we want the new music to be 3 bars long.
'''
num_bars = 3
'''
generation_start_time is set to primer_end_time, which means the new music will start playing after the drum pattern ends. 
'''
generation_start_time = primer_end_time
'''
generation_end_time is calculated as generation_start_time plus seconds_per_bar multiplied by num_bars, which means the new music will 
end playing after 3 bars. The two print statements are just to show the start and end time of both the drum pattern and the new music.'''
generation_end_time = generation_start_time + (seconds_per_bar * num_bars)

print(f"Primer start and end:"
        f"[{primer_start_time}, {primer_end_time}]")
print(f"Generation start and end:"
        f"[{generation_start_time}, {generation_end_time}]")

'''
Here, we are setting the options for generating the new music. The GeneratorOptions object is created, 
which allows us to specify certain parameters for the music generation. The temperature option is set to 1.0,
which means the new music will be generated with a default level of randomness. The generate_sections option is 
set with start_time and end_time so that the new music is generated only within the specified time range.
 '''
from note_seq.protobuf import generator_pb2
generator_options = generator_pb2.GeneratorOptions()
generator_options.args['temperature'].float_value = 1.0  # Higher is more random; 1.0 is default.
generator_options.generate_sections.add(start_time=generation_start_time, end_time = generation_end_time)
'''
This line generates the new music using the generator object and the primer_sequence 
we created before, with the options specified in generator_options. 
The result is stored in the sequence variable.

This line generates a new piece of music based on the primer_sequence and the generator_options.
The generator is a machine learning model that was trained on lots of music data and it knows 
how to create new pieces that are similar to the primer_sequence while still being original.
'''
sequence = generator.generate(primer_sequence, generator_options)

'''
This line imports a module called Plotter from the visual_midi library. 
The Plotter module allows us to display a graphical representation of the generated music.
'''
from visual_midi import Plotter
'''
#write the result to a midi file
#This line creates a new file with the name "outputX.mid" in a directory called
#"output". The .mid extension stands for "Musical Instrument Digital Interface", 
#which is a file format for storing music.
'''

midi_file = os.path.join("output", "outputX.mid")

'''
This line writes the generated sequence to the midi_file that was created in the previous line.
This means that the generated music is saved as a MIDI file so that it can be played and shared with others.
'''
mm.midi_io.note_sequence_to_midi_file(sequence, midi_file)
print(f"Generated midi file: {os.path.abspath(midi_file)}")

# Write the resulting plot file to the output directory
'''
This line imports another library called pretty_midi. The pretty_midi library 
allows us to display a graphical representation of the generated music in a web browser
'''
from pretty_midi import PrettyMIDI

plot_file = os.path.join("output", "outputX.html")
# pretty_midi = mm.midi_io.note_sequence_to_pretty_midi(sequence = sequence).write(plot_file)
'''
This line reads the midi_file that was created in step 4 and converts it into a pretty_midi object that can be displayed in a web browser.
'''
pretty_midi = PrettyMIDI("C:\Mandil\co-op\hands-on-music-generation-with-magenta\Chapter02\output\outputX.mid")
print(f"Generated plot file: {os.path.abspath(plot_file)}")
plotter = Plotter()
plotter.show(pretty_midi, plot_file)
print(f"Generated plot file: {os.path.abspath(plot_file)}")

'''
The reason the code was written is to convert the generated music into a file format that can be played and shared with others. 
The code also creates a graphical representation of the generated music so that it can be easily viewed and appreciated.'''