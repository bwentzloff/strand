# Strand Interpreter

The **Strand Interpreter** is an esoteric programming language designed to execute DNA sequences as code. Inspired by genetic programming, it supports direct DNA sequence inputs, FASTA file formats, and virus libraries in FASTA format.

---

## Features
1. **DNA Sequence Execution**:
   - Interpret DNA sequences directly.
   - Supports start (`ATG`) and stop (`TAA`, `TAG`, `TGA`) codons.
   - Segmented pathways for modular execution.

2. **FASTA File Support**:
   - Read and interpret sequences from FASTA files.

3. **Virus Libraries in FASTA Format**:
   - Extend functionality using "virus libraries" identified by codon strings.
   - Virus libraries include metadata and license details in the FASTA header.

4. **Final Outputs**:
   - **Textual Logs**: Summarize synthesized proteins.
   - **Numerical Results**: Binary arithmetic pathways.
   - **Visual Graphs**: Render pathway interactions (planned).

---

## Usage
### Direct DNA Sequence Input
Run a DNA sequence directly:
```bash
strand ATGACCGATTAA
```

### FASTA File Input
Run a DNA sequence from a FASTA file:
```bash
strand -f example.fasta
```

### Virus Library and DNA Input
Run a DNA sequence with a virus library in FASTA format:
```bash
strand -vf virus_addition.fasta example.fasta
```

---

## Example Virus Library (FASTA)
```plaintext
>Virus_Addition | License: MIT
AAGGTTCCCGAT
```

---

## Example Programs
### Basic Protein Synthesis
Input:
```plaintext
ATG ACC GAT TAA
```
Output:
```plaintext
Results:
Proteins: [['Protein_X', 'Transport']]
Environment: {'TEMP': 'NEUTRAL', 'ENERGY': 'MEDIUM'}
```

### Using Virus Libraries
Input:
```bash
strand -vf virus_addition.fasta example.fasta
```
Output:
```plaintext
Loaded Virus: Virus_Addition | License: MIT
Results:
Proteins: [['Protein_X', 'Transport', 'Protein_Sum']]
Environment: {'TEMP': 'NEUTRAL', 'ENERGY': 'MEDIUM'}
```

---

## Example Use Cases

### 1. Basic Protein Synthesis
DNA Sequence:
```plaintext
ATG ACC GAT TAA
```
Output:
```plaintext
Proteins: ["Protein_X", "Transport"]
Environment: {"TEMP": "NEUTRAL", "ENERGY": "MEDIUM"}
```

### 2. Arithmetic Operations with Virus
DNA Sequence (with Virus Library):
```plaintext
TAA AAGGTTCCCGAT ATG ACC GAT TAA
```
Output:
```plaintext
Loaded Virus: Virus_Addition
Proteins: ["Protein_X", "Transport", "Protein_Sum"]
Environment: {"TEMP": "NEUTRAL", "ENERGY": "MEDIUM"}
```

### 3. Pathway Visualization
DNA Sequence:
```plaintext
ATG ACC GAT CCG TAA
```
Visualization:
- Nodes: `Start`, `Protein_X`, `Transport`, `Synthesis`
- Edges: Represent transitions between proteins.

### 4. Using FASTA Files
FASTA File:
```plaintext
>Basic Protein Synthesis
ATG ACC GAT TAA
```
Run with the interpreter:
```bash
strand -f examples/basic_protein_synthesis.fasta
```
Output:
```plaintext
Proteins: ["Protein_X", "Transport"]
Environment: {"TEMP": "NEUTRAL", "ENERGY": "MEDIUM"}
```

### 5. Advanced: Virus-Modified Pathways
DNA Sequence (with Virus Library):
```plaintext
TAA MIDI123456 ATG ACC GAT TAA
```
Output:
```plaintext
Loaded Virus: MIDI_Virus
Results:
Proteins: ["Protein_X", "Transport", "MIDI_Stream"]
Environment: {"TEMP": "NEUTRAL", "ENERGY": "MEDIUM"}
```

Additional functionality allows the output to be converted into MIDI format for audio generation.

### 6. Real-World Simulation
Example DNA Sequence:
```plaintext
ATG GGG TAA ATG ACC GAT TAA
```
Output:
```plaintext
Proteins: ["Energy_Transfer", "Protein_X", "Transport"]
Environment: {"TEMP": "HIGH", "ENERGY": "MEDIUM"}
```

### Visualization Example
- The visualization will display:
  - Nodes: `Start`, `Energy_Transfer`, `Protein_X`, `Transport`
  - Edges: Arrows connecting each protein and showing environmental influences.

---

## Documentation

Explore the full Strand documentation [here](https://<your-username>.github.io/strand/).

## License
MIT License. See LICENSE file for details.
