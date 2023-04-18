import os
from typing import List
import magenta.music as mm
import tensorflow as tf
from magenta.models.music_vae import TrainedModel, configs
from magenta.music import DEFAULT_STEPS_PER_BAR
from note_seq.protobuf.music_pb2 import NoteSequence
from six.moves import urllib
from note_seq.midi_io import note_sequence_to_midi_file
from .helper_utils import save_midi, save_plot

class MusicGeneratorVAE:
    def __init__(self):
        self.num_output = 6
        self.num_bar_per_sample = 2
        self.num_steps_per_sample = self.num_bar_per_sample * DEFAULT_STEPS_PER_BAR
        self.total_bars = self.num_output * self.num_bar_per_sample
        self.drum_model = self.get_model("nade-drums_2bar_full")
        self.piano_model = self.get_model("cat-mel_2bar_big")
        self.groove_model = self.get_model("groovae_2bar_humanize")

    def download_checkpoint(self, model_name, checkpoint_name, target_dir):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        checkpoint_target = os.path.join(target_dir, checkpoint_name)
        print(checkpoint_target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        if not os.path.exists(checkpoint_target):
            response = urllib.request.urlopen(
                f"https://storage.googleapis.com/magentadata/models/"
                f"{model_name}/checkpoints/{checkpoint_name}")
            data = response.read()
            local_file = open(checkpoint_target, 'wb')
            local_file.write(data)
            local_file.close()

    def get_model(self, name):
        print("im here at get_model function")
        checkpoint = name + ".tar"
        if not os.path.exists("checkpoints/" + checkpoint):
            self.download_checkpoint("music_vae", checkpoint, "checkpoints")
            return TrainedModel(
                    configs.CONFIG_MAP[name.split(".")[0] if "." in name else name],
                    batch_size=8,
                    checkpoint_dir_or_path=os.path.join("checkpoints", checkpoint))
        else:
            return TrainedModel(
                configs.CONFIG_MAP[name.split(".")[0] if "." in name else name],
                batch_size=8,
                checkpoint_dir_or_path=os.path.join("checkpoints", checkpoint))
        
    #drums
    def sample(self,model_name, num_steps_per_sample,filename,create_file=False):
        
        model = self.drum_model
        num_steps_per_sample = self.num_bar_per_sample * DEFAULT_STEPS_PER_BAR
        sample_sequences = model.sample(n=2, length=num_steps_per_sample)
        if create_file:
            save_midi(sample_sequences, "sample", model_name,filename)
        return sample_sequences

    #piano
    def interpolate(self, model_name, num_steps_per_sample, num_output,filename,create_file=False):
        model = self.piano_model
        sample_sequences = model.sample(n=2, length=self.num_steps_per_sample)
        print("sample_sequences",len(sample_sequences))
        if len(sample_sequences) != 2:
            raise Exception(f"Wrong number of sequences, expected: 2, actual: {len(sample_sequences)}")
        if not sample_sequences[0].notes or not sample_sequences[1].notes:
            raise Exception(f"Empty note sequences, sequence 1 length: {len(sample_sequences[0].notes)}, sequence 2 length: {len(sample_sequences[1].notes)}")
        
        interpolate_sequences = model.interpolate(
            start_sequence=sample_sequences[0],
            end_sequence=sample_sequences[1],
            num_steps=self.num_output,
            length=self.num_steps_per_sample)

        interpolate_sequence = mm.sequences_lib.concatenate_sequences(interpolate_sequences, [4] * num_output)
        if create_file:
            save_midi(interpolate_sequence, "merge", model_name,filename)

        return interpolate_sequence

    #mix-
    def groove(self, model_name, interpolate_sequence, num_steps_per_sample, num_output,filename):
        # num_steps_per_sample = self.num_steps_per_sample
        # sample_sequences = self.sample("cat-drums_2bar_small.lokl", num_steps_per_sample, filename)
        # interpolate_sequence = self.interpolate("cat-drums_2bar_small.hikl",sample_sequences, num_steps_per_sample, self.num_output,filename)
        model = self.groove_model
        # split_interpolate_sequences = mm.sequences_lib.split_note_sequence(interpolate_sequence, 4)

        # if len(split_interpolate_sequences) != num_output:
        #     raise Exception(f"Wrong number of interpolate size, expected: 10, actual: {len(split_interpolate_sequences)}")

        # encoding, mu, sigma = model.encode(note_sequences=split_interpolate_sequences)
        # groove_sequences = model.decode(z=encoding, length=num_steps_per_sample)
        # groove_sequence = mm.sequences_lib.concatenate_sequences(groove_sequences, [4] * num_output)
        groove_sequence = model.sample(n=2, length=num_steps_per_sample)

        save_midi(groove_sequence, "groove", model_name,filename)
        return groove_sequence
    
    def generate_music(self,filename):
        generated_sample_sequences = self.sample("cat-drums_2bar_small.lokl", self.num_steps_per_sample,filename)
        generated_interpolate_sequence = self.interpolate("cat-drums_2bar_small.hikl", generated_sample_sequences, self.num_steps_per_sample, self.num_output, self.total_bars,filename)
        generated_groove_sequence = self.groove("groovae_4bar", generated_interpolate_sequence, self.num_steps_per_sample, self.num_output, self.total_bars,filename)

        print(f"Generated groove sequence total time: {generated_groove_sequence.total_time}")

        return generated_groove_sequence