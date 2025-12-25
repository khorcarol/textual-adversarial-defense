import json
import random

try:
    # When installed as a package
    from textual_adversarial_defense.resources import load_json_resource
except ImportError:
    # For local development, use direct path
    from pathlib import Path
    import os
    
    def load_json_resource(relative_path: str) -> dict:
        # Get the utils directory relative to this file
        current_dir = Path(__file__).parent.parent
        resource_path = current_dir / "utils" / relative_path
        with open(resource_path, 'r', encoding='utf-8') as f:
            return json.load(f)

# Bidi override characters
LRO = chr(0x202D)  # Left-to-Right Override
RLO = chr(0x202E)  # Right-to-Left Override
LRI = chr(0x2066)  # Left-to-Right Isolate
RLI = chr(0x2067)  # Right-to-Left Isolate
PDI = chr(0x2069)  # Pop Directional Isolate
PDF = chr(0x202C)  # Pop Directional Formatting



class TagAttack:
    def __init__(self, perturbation_budget, tags= [0xE0001,*range(0xE0020, 0xE007F+1)]):
        self.perturbation_budget = perturbation_budget
        self.tags = tags

    def perturb(self, text):
        """
        Insert random Unicode tag characters into text, treating each
        Unicode codepoint as a single character.
        """
        # Convert string to list of codepoints
        codepoints = [ord(c) for c in text]

        for i in range(self.perturbation_budget):
            # Choose random position in codepoint list
            rand_index = random.randrange(len(codepoints) + 1)  # +1 to allow appending
            rand_tag = random.choice(self.tags)

            # Insert the tag codepoint at the chosen position
            codepoints.insert(rand_index, rand_tag)

        # Convert back to string
        return "".join(chr(cp) for cp in codepoints)


class VariationSelectorAttack:
    def __init__(self, perturbation_budget, variation_selectors = [*range(0xFE00, 0xFE0F + 1), *range(0xE0100, 0xE01EF + 1)]):
        self.perturbation_budget = perturbation_budget
        self.variation_selectors = variation_selectors

    def perturb(self, text):
        # Convert string to list of codepoints
        codepoints = [ord(c) for c in text]

        for _ in range(self.perturbation_budget):
            # Choose random position in codepoint list
            rand_index = random.randrange(len(codepoints) + 1)  # allow append
            rand_vs = random.choice(self.variation_selectors)

            # Insert the variation selector codepoint
            codepoints.insert(rand_index, rand_vs)

        # Convert back to string
        return "".join(chr(cp) for cp in codepoints)


class InvisibleCharAttack:
    def __init__(self, perturbation_budget, invisible_chars=[0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF]):
        self.perturbation_budget = perturbation_budget
        self.invisible_chars = invisible_chars

    def perturb(self, text):
        # Convert string to list of codepoints
        codepoints = [ord(c) for c in text]

        for _ in range(self.perturbation_budget):
            # Choose random position in codepoint list
            rand_index = random.randrange(len(codepoints) + 1)  # allow append
            rand_invisible = random.choice(self.invisible_chars)

            # Insert the invisible character
            codepoints.insert(rand_index, rand_invisible)

        # Convert back to string
        return "".join(chr(cp) for cp in codepoints)


class HomoglyphAttack:
    def __init__(self, perturbation_budget, homoglyph_map_path=None):
        self.perturbation_budget = perturbation_budget
        
        if homoglyph_map_path is None:
            # Load from package resources (works for both wheel and local)
            hex_map = load_json_resource("homoglyphs/intentional.json")
        else:
            # Allow override with explicit path for backward compatibility
            with open(homoglyph_map_path, 'r', encoding='utf-8') as f:
                hex_map = json.load(f)
        
        # The JSON has sanitizer mappings: Suspicious -> Legitimate (e.g., Cyrillic -> Latin)
        # For attacks, we need the reverse: Legitimate -> Suspicious (e.g., Latin -> Cyrillic)
        # So we reverse the mapping for the attack
        self.homoglyph_map = {int(v, 16): int(k, 16) for k, v in hex_map.items()}
        self.homoglyph_chars = list(self.homoglyph_map.keys())

    def perturb(self, text):
        # Convert string to list of codepoints
        codepoints = [ord(c) for c in text]
        
        # Replace random characters with homoglyphs
        indices = list(range(len(codepoints)))
        random.shuffle(indices)
        
        for i in indices[:min(self.perturbation_budget, len(indices))]:
            cp = codepoints[i]
            # If character has a homoglyph, replace it
            if cp in self.homoglyph_map:
                codepoints[i] = self.homoglyph_map[cp]

        # Convert back to string
        return "".join(chr(cp) for cp in codepoints)


class DeletionCharAttack:
    def __init__(self, perturbation_budget, deletion_char=0x8):
        self.perturbation_budget = perturbation_budget
        self.deletion_char = deletion_char  # Backspace character
        self.ascii_chars = list(range(32, 127))  # Printable ASCII characters

    def perturb(self, text):
        # Convert string to list of codepoints
        codepoints = [ord(c) for c in text]
        
        for _ in range(self.perturbation_budget):
            # Choose random position in codepoint list
            rand_index = random.randrange(len(codepoints) + 1)  # allow append
            # Insert random ASCII character followed by deletion character
            rand_ascii = random.choice(self.ascii_chars)
            codepoints.insert(rand_index, rand_ascii)
            codepoints.insert(rand_index + 1, self.deletion_char)

        # Convert back to string
        return "".join(chr(cp) for cp in codepoints)


class BidiAttack:
    def __init__(self, perturbation_budget):
        self.perturbation_budget = perturbation_budget
    
    def _encode_swap_spoof(self, one, two):
        """
        Creates a string that contains the characters 'two' followed by 'one' 
        in the data, but is displayed as 'one' followed by 'two'.
        Sequence: RLO + two + one + PDF
        """
        # LRO, LRI, RLO, LRI, el.two, PDI, LRI, el.one, PDI, PDF, PDI, PDF
        
        # Display order is visually reversed by RLO
        return LRO + LRI+ RLO + LRI + two + PDI + LRI + one + PDI + PDF + PDI + PDF

    def perturb(self, text):
        """
        Swaps random *non-overlapping* adjacent character pairs in the 
        underlying data and uses Bidi controls to visually reverse the swap.
        """
        chars = list(text)
        n = len(chars)
        
        possible_start_indices = list(range(n - 1))
        random.shuffle(possible_start_indices)
        
        swaps_to_make = set()
        swaps_remaining = self.perturbation_budget
        
        # Select non-overlapping swap positions
        for i in possible_start_indices:
            if i not in swaps_to_make and i + 1 not in swaps_to_make:
                if swaps_remaining > 0:
                    swaps_to_make.add(i)
                    # Add the next index to the set to prevent it from starting a new swap
                    swaps_to_make.add(i + 1) 
                    swaps_remaining -= 1
                else:
                    break

        swaps_to_make = []
        available_positions = list(range(n - 1))
        random.shuffle(available_positions)
        
        processed_indices = set()
        
        for pos in available_positions:
            # A swap starts at 'pos' and involves 'pos' and 'pos + 1'
            if pos not in processed_indices and (pos + 1) not in processed_indices:
                if len(swaps_to_make) < self.perturbation_budget:
                    swaps_to_make.append(pos)
                    # Mark both characters in the pair as 'used'
                    processed_indices.add(pos)
                    processed_indices.add(pos + 1)
                else:
                    break
        
        
        # Build perturbed text
        perturbed_text = ""
        i = 0
        while i < n:
            if i in swaps_to_make and chars[i].isalpha() and chars[i + 1].isalpha():
                # This index starts a swap
                char_one = chars[i]
                char_two = chars[i + 1]
                
                # Data: two, one (visually displays as: one, two)
                spoofed_pair = self._encode_swap_spoof(char_one, char_two)
                perturbed_text += spoofed_pair
                
                # Advance counter by 2 since both characters were processed
                i += 2 
            else:
                # Add normal character
                perturbed_text += chars[i]
                i += 1
                
        return perturbed_text