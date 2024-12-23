# Advanced Use Case: Generating MIDI Streams

## Overview
The Strand language can output MIDI-compatible streams using a specialized virus. This virus formats numeric outputs into a sequence of MIDI notes and velocities. These outputs can then be fed into external tools to generate audio.

## MIDI Virus Implementation
The MIDI virus converts numeric proteins into MIDI-compatible values:
- **Note Values**: Numeric proteins are mapped to MIDI notes (0–127).
- **Velocity**: Default velocity is set to 64.

### Virus FASTA File
```plaintext
>MIDI_Virus | License: MIT
MIDI123456
```

### Sample DNA Program
DNA Sequence (with MIDI Virus):
```plaintext
TAA MIDI123456 ATG GGG TGA
```

### Expected Output
```plaintext
Loaded Virus: MIDI_Virus | License: MIT
Results:
Proteins: [(60, 64), (62, 64), (64, 64)]
Environment: {'TEMP': 'NEUTRAL', 'ENERGY': 'MEDIUM'}
```

## Using the Output
The output is a list of MIDI-compatible tuples `(note, velocity)`:
1. Save the output to a file (e.g., `output.midi`).
2. Use a tool like `mido` or a DAW to play or render the MIDI stream.

### Example: Using Python and Mido
```python
import mido

midi_stream = [(60, 64), (62, 64), (64, 64)]  # Example output from the interpreter

# Create a MIDI file
midi_file = mido.MidiFile()
track = mido.MidiTrack()
midi_file.tracks.append(track)

for note, velocity in midi_stream:
    track.append(mido.Message('note_on', note=note, velocity=velocity, time=0))
    track.append(mido.Message('note_off', note=note, velocity=0, time=200))

midi_file.save('output.midi')
```

### Play the MIDI File
You can now play `output.midi` using your favorite DAW or MIDI player.