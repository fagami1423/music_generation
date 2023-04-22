"""
Common utilities for the book's code.
"""

import os
import time
from pathlib import Path
from typing import Union, List, Optional

import magenta.music as mm
from note_seq.protobuf.music_pb2 import NoteSequence
from visual_midi import Plotter
from midi2audio import FluidSynth


   
def convert_midi_to_wav(input_midi: str, output_wav: str, soundfont: str = 'path/to/soundfont.sf2'):
    fs = FluidSynth(soundfont)
    fs.midi_to_audio(input_midi, output_wav)

#write a function that checks the midi of different folders and check if they are converted into wav format or not and save them to a specific folder
#write a function that checks the midi of different folders and check if they are converted into wav format or not and save them to a specific folder
def convert_midi_files_in_folder(midi_folder: str, wav_folder: str,filename: str, soundfont: str = 'path/to/soundfont.sf2'):
    midi_folder_path = Path(midi_folder)
    wav_folder_path = Path(wav_folder)
    print("midi_folder_path",midi_folder_path)
    print("wav_folder_path",wav_folder_path)

    wav_folder_path.mkdir(parents=True, exist_ok=True)

    for midi_file in midi_folder_path.glob('*.mid'):
        wav_file = f"{midi_file.stem}.wav"
        output_wav_path = wav_folder_path / wav_file
        print(str(midi_file))
        print("output_wav_path",output_wav_path)
        if not output_wav_path.exists():
            print(f"Converting {midi_file} to {output_wav_path}")
            convert_midi_to_wav(str(midi_file), str(output_wav_path), soundfont)
        else:
            print(f"{output_wav_path} already exists")

def save_midi(sequences: Union[NoteSequence, List[NoteSequence]],
              output_dir: Optional[str] = None,
              prefix: str = "sequence",
              filename: str = "sample"):
    """
    Writes the sequences as MIDI files to the "output" directory, with the
    filename pattern "<prefix>_<index>_<date_time>" and "mid" as extension.
        :param sequences: a NoteSequence or list of NoteSequence to be saved
        :param output_dir: an optional subdirectory in the output directory
        :param prefix: an optional prefix for each file
    """
    output_dir = os.path.join("output", output_dir) if output_dir else "output"
    os.makedirs(output_dir, exist_ok=True)
    if not isinstance(sequences, list):
        sequences = [sequences]
    original_filename = filename
    for (index, sequence) in enumerate(sequences):
        date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
        filename = f"{filename}_{date_and_time}.mid"
        path = os.path.join(output_dir, filename)
        mm.midi_io.note_sequence_to_midi_file(sequence, path)
        print(f"Generated midi file: {os.path.abspath(path)}")
    # outfile = path.split(".mid")[0]
    print("Converting midi to wav")
    convert_midi_files_in_folder(os.path.abspath(output_dir),os.path.abspath("music"),"default.sf2") 
    print("Conversion complete")
    return path

def save_plot(sequences: Union[NoteSequence, List[NoteSequence]],
              output_dir: Optional[str] = None,
              prefix: str = "sequence",
              **kwargs):
    """
    Writes the sequences as HTML plot files to the "output" directory, with the
    filename pattern "<prefix>_<index>_<date_time>" and "html" as extension.
        :param sequences: a NoteSequence or list of NoteSequence to be saved
        :param output_dir: an optional subdirectory in the output directory
        :param prefix: an optional prefix for each file
        :param kwargs: the keyword arguments to pass to the Plotter instance
    """
    output_dir = os.path.join("output", output_dir) if output_dir else "output"
    os.makedirs(output_dir, exist_ok=True)
    if not isinstance(sequences, list):
        sequences = [sequences]
    for (index, sequence) in enumerate(sequences):
        date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
        filename = f"{prefix}_{index:02}_{date_and_time}.html"
        path = os.path.join(output_dir, filename)
        midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
        plotter = Plotter(**kwargs)
        plotter.save(midi, path)
        print(f"Generated plot file: {os.path.abspath(path)}")