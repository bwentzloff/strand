import json

def parse_environment_block(codons):
    """Parse an environment block from the DNA."""
    environment = {"TEMP": "LOW", "ENERGY": "LOW"}
    env_name_codons = []
    i = 0

    # Capture environment name until a recognizable TEMP codon or 'TAA'
    while i < len(codons) and codons[i] not in ["AAA", "AAT", "AAC", "TAA"]:
        env_name_codons.append(codons[i])
        i += 1

    # Decode environment name or set a default if none exists
    if env_name_codons:
        environment["Name"] = decode_dna_to_string(" ".join(env_name_codons))
    else:
        environment["Name"] = f"Unnamed_Env_{id(environment)}"

    # Stop parsing if 'TAA' is encountered
    if i < len(codons) and codons[i] == "TAA":
        return environment, i + 1

    # Process TEMP
    if i < len(codons) and codons[i] in ["AAA", "AAT", "AAC"]:
        environment["TEMP"] = {
            "AAA": "HIGH",
            "AAT": "MEDIUM",
            "AAC": "LOW"
        }[codons[i]]
        i += 1

    # Process ENERGY
    if i < len(codons) and codons[i] in ["GGA", "GGC", "GGG"]:
        environment["ENERGY"] = {
            "GGA": "HIGH",
            "GGC": "MEDIUM",
            "GGG": "LOW"
        }[codons[i]]
        i += 1

    return environment, i

def decode_dna_to_string(dna):
    """Decode a DNA sequence into a string using base-6 encoding."""
    codon_to_base6 = {"AAA": 0, "AAC": 1, "AAG": 2, "ACA": 3, "ACC": 4, "ACG": 5}
    codons = dna.split()
    base6_digits = [codon_to_base6[codon] for codon in codons]
    chars = []
    ascii_value = 0
    multiplier = 1
    for digit in reversed(base6_digits):
        ascii_value += digit * multiplier
        multiplier *= 6
        if multiplier == 216:  # Reset after every 3 digits (base-6 codons)
            chars.append(chr(ascii_value))
            ascii_value = 0
            multiplier = 1
    if ascii_value > 0:
        chars.append(chr(ascii_value))
    return "".join(reversed(chars))

def modify_pathway(environment, pathway, tick):
    """Modify pathways dynamically based on the environment and tick."""
    # Placeholder for pathway modification logic
    return pathway

def interpret_dna_with_ticks(dna, max_ticks=10):
    """Interpret DNA and output JSON for relevant ticks."""
    codons = dna.split()
    print("Processing DNA sequence:", dna)
    print("Codons:", codons)

    interpretation = {"Environments": {}, "Pathways": []}
    current_index = 0

    try:
        # Parse environments
        while current_index < len(codons):
            if codons[current_index] == "TGC":
                environment, next_index = parse_environment_block(codons[current_index + 1:])
                interpretation["Environments"][environment["Name"]] = environment
                current_index += next_index + 1
                print("Parsed environment:", environment)
            else:
                break

        # Parse pathways
        while current_index < len(codons):
            if codons[current_index] == "ATG":
                print("Parsing pathway starting at index", current_index)
                # Ensure there are enough codons for a pathway
                if current_index + 3 < len(codons):
                    interpretation["Pathways"].append({
                        "Nodes": [codons[current_index + 1], codons[current_index + 2], codons[current_index + 3]],
                        "Edges": [[codons[current_index + 1], codons[current_index + 2]], 
                                  [codons[current_index + 2], codons[current_index + 3]]]
                    })
                    current_index += 4
                else:
                    print(f"Incomplete pathway definition at index {current_index}: {codons[current_index:]}")
                    break
            elif codons[current_index] == "TAA":  # Stop codon
                print("Encountered stop codon 'TAA'. Ending pathway parsing.")
                break
            else:
                proteins.append(action)
    return proteins

def interpret_dna(sequence):
    """Interpret a DNA sequence and return results."""
    proteins = []
    environment = {"TEMP": "NEUTRAL", "ENERGY": "MEDIUM"}
    viruses = []

    # Parse the DNA sequence into codons
    codons = [sequence[i:i+3] for i in range(0, len(sequence), 3)]

    # Process environment variables (first 3 codons)
    env_codon_map = {
        "AAA": ("TEMP", "HIGH"),
        "TTT": ("TEMP", "LOW"),
        "GGG": ("ENERGY", "HIGH"),
        "CCC": ("ENERGY", "LOW"),
    }
    for codon in codons[:3]:
        if codon in env_codon_map:
            key, value = env_codon_map[codon]
            environment[key] = value

    # Process program codons (after environment setup)
    codon_map = {
        "ACC": "Protein_X",
        "GAT": "Transport",
        "CCG": "Synthesis",
    }

    # Simulate virus repository
    virus_repository = {
        "TGGACCTGA": {"name": "MIDI_Virus", "function": "MIDI_Stream"},
    }

    for i in range(3, len(codons)):
        codon = codons[i]
        # Check if the codon matches a known virus sequence
        if i + 2 < len(codons):
            virus_codon = "".join(codons[i:i+3])
            if virus_codon in virus_repository:
                virus_data = virus_repository[virus_codon]
                viruses.append(virus_data["name"])
                proteins.append(virus_data["function"])
                break  # Skip processing the remaining virus codons
        elif codon in codon_map:
            proteins.append(codon_map[codon])

    return {
        "Proteins": proteins,
        "Environment": environment,
        "Viruses": viruses,
    }


if __name__ == "__main__":
    import sys

    # Check for command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <DNA sequence>")
        sys.exit(1)

    # Handle special flags
    dna = sys.argv[1]
    if dna.lower() == "--help":
        print("""
Strand Interpreter
Usage: python interpreter.py <DNA sequence>

Options:
  --help        Show this help message

Example:
  python interpreter.py "TGC TAA ACC GAT TAA"
        """)
        sys.exit(0)

    # Validate DNA sequence
    if not all(c in "ACTG " for c in dna):
        print(f"Error: Invalid DNA sequence: Must only contain A, C, T, G.")
        sys.exit(1)

    # Interpret the DNA sequence
    try:
        results = interpret_dna_with_ticks(dna)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error interpreting DNA: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
