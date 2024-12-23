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

## Documentation

Explore the full Strand documentation [here](https://<your-username>.github.io/strand/).

## License
MIT License. See LICENSE file for details.
