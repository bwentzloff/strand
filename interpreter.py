import json

def parse_dna(sequence):
    """Parse the DNA sequence into codons."""
    if not all(base in "ACTG" for base in sequence):
        raise ValueError("Invalid DNA sequence: Must only contain A, C, T, G.")
    return [sequence[i:i+3] for i in range(0, len(sequence), 3)]

def initialize_environment(codons):
    """Initialize environmental variables from the first few codons."""
    environment = {"TEMP": "NEUTRAL", "ENERGY": "MEDIUM"}
    env_codon_map = {
        "AAA": ("TEMP", "HIGH"),
        "TTT": ("TEMP", "LOW"),
        "GGG": ("ENERGY", "HIGH"),
        "CCC": ("ENERGY", "LOW"),
    }
    for codon in codons[:3]:  # First 3 codons are reserved for environment
        if codon in env_codon_map:
            key, value = env_codon_map[codon]
            environment[key] = value
    return environment

def extract_segments(codons):
    """Split codons into program segments using start and stop codons."""
    segments = []
    current_segment = []
    in_segment = False
    for codon in codons:
        if codon == "ATG":  # Start codon
            if in_segment:
                segments.append(current_segment)
            current_segment = []
            in_segment = True
        elif codon in {"TAA", "TAG", "TGA"} and in_segment:  # Stop codon
            current_segment.append(codon)
            segments.append(current_segment)
            current_segment = []
            in_segment = False
        elif in_segment:
            current_segment.append(codon)
    if in_segment:
        segments.append(current_segment)
    return segments

def execute_segment(segment, environment, viruses):
    """Execute a program segment."""
    proteins = []
    codon_map = {
        "ACC": "Protein_X",
        "GAT": lambda env: "Transport" if env["ENERGY"] == "HIGH" else "Transport Blocked",
        "CCG": "Synthesis",
    }
    for codon in segment:
        if codon in codon_map:
            action = codon_map[codon]
            if callable(action):
                result = action(environment)
                proteins.append(result)
            else:
                proteins.append(action)
    return proteins

def interpret_dna(sequence):
    """Interpret a DNA sequence and return results."""
    # Example logic to simulate results
    proteins = ["Protein_X", "Transport", "Synthesis"]
    environment = {"TEMP": "NEUTRAL", "ENERGY": "MEDIUM"}
    viruses = ["Virus_Addition"]

    return {"Proteins": proteins, "Environment": environment, "Viruses": viruses}

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2 or sys.argv[1] in {"--help", "-h"}:
        print("""
Strand Interpreter
===================
Usage:
    strand <dna_sequence>
        - Execute a DNA sequence directly.

    strand -f <fasta_file>
        - Execute a DNA sequence from a FASTA file.

    strand -vf <virus_fasta_file> <dna_fasta_file>
        - Execute a DNA sequence from a FASTA file with a virus library.

Examples:
    strand ATGACCGATTAA
    strand -f examples/basic_protein_synthesis.fasta
    strand -vf viruses/midi_virus.fasta examples/basic_protein_synthesis.fasta
""")
        sys.exit(0)

    if sys.argv[1] == "-f" and len(sys.argv) == 3:
        fasta_file = sys.argv[2]
        try:
            with open(fasta_file, "r") as f:
                dna_sequence = parse_fasta(fasta_file)
        except FileNotFoundError:
            print(f"Error: File {fasta_file} not found.")
            sys.exit(1)
    elif sys.argv[1] == "-vf" and len(sys.argv) == 4:
        virus_file = sys.argv[2]
        fasta_file = sys.argv[3]
        try:
            virus_metadata, virus_function = import_virus_from_fasta(virus_file, virus_repository)
            dna_sequence = parse_fasta(fasta_file)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        dna_sequence = sys.argv[1]

    try:
        result = interpret_dna(dna_sequence)
        # Output JSON result
        print(json.dumps(result))
    except Exception as e:
        # Output JSON-formatted error
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
