import os
import magenta.music as mm
from magenta.models.shared import sequence_generator_bundle
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.music import constants

bundle_file = os.path.join("bundles", "drum_kit_rnn.mag")
bundle = sequence_generator_bundle.read_bundle_file(bundle_file)

generator_map = drums_rnn_sequence_generator.get_generator_map()
generator = generator_map["drum_kit"](checkpoint=None, bundle=bundle)
generator.initialize()

QPM = 120
seconds_per_step = 60.0 / QPM / generator.steps_per_quarter
steps_per_bar = constants.DEFAULT_STEPS_PER_BAR
seconds_per_bar = steps_per_bar * seconds_per_step

primer_drums = mm.DrumTrack([frozenset(pitches) for pitches in [
    (38, 51), (), (36,), (),
    (38, 44, 51), (), (36,), (),
    (), (), (38,), (),
    (38, 44), (), (36, 51), (),
]])
primer_sequence = primer_drums.to_sequence(qpm=QPM)

primer_start_time = 0
primer_end_time = primer_start_time + seconds_per_bar
num_bars = 3
generation_start_time = primer_end_time
generation_end_time = generation_start_time + num_bars * seconds_per_bar

generated_sequence = generator.generate(
    primer_sequence=primer_sequence,
    primer_start_time=primer_start_time,
    primer_end_time=primer_end_time,
    generation_start_time=generation_start_time,
    generation_end_time=generation_end_time
)

output_file = "generated_drum_track.mid"
mm.sequence_proto_to_midi_file(generated_sequence, output_file)

# import os
# import magenta.music as mm
# from magenta.models.shared import sequence_generator_bundle
# from magenta.models.drums_rnn import drums_rnn_sequence_generator
# from magenta.music import constants
#
# bundle_dir = "bundles"
# bundle_file = os.path.join(bundle_dir, "drum_kit_rnn.mag")
# bundle = sequence_generator_bundle.read_bundle_file(bundle_file)
#
# generator_map = drums_rnn_sequence_generator.get_generator_map()
# generator = generator_map["drum_kit"](checkpoint=None, bundle=bundle)
# generator.initialize()
#
# QPM = 120
# steps_per_quarter = generator.steps_per_quarter
# seconds_per_step = 60.0 / QPM / steps_per_quarter
# steps_per_bar = constants.DEFAULT_STEPS_PER_BAR
# seconds_per_bar = steps_per_bar * seconds_per_step
#
# primer_drums = mm.DrumTrack([frozenset(pitches) for pitches in [
#     (38, 51), (), (36,), (),
#     (38, 44, 51), (), (36,), (),
#     (), (), (38,), (),
#     (38, 44), (), (36, 51), (),
# ]])
# primer_sequence = primer_drums.to_sequence(qpm=QPM)
#
# primer_start_time = 0
# primer_end_time = primer_start_time + seconds_per_bar
# num_bars = 3
# generation_start_time = primer_end_time
# generation_end_time = generation_start_time + num_bars * seconds_per_bar
#
# generated_sequence = generator.generate(
#     primer_sequence=primer_sequence,
#     primer_start_time=primer_start_time,
#     primer_end_time=primer_end_time,
#     generation_start_time=generation_start_time,
#     generation_end_time=generation_end_time
# )
#
# output_file = "generated_drum_track.mid"
# mm.sequence_proto_to_midi_file(generated_sequence, output_file)

