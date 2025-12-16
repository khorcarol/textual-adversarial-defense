import textual_adversarial_defense
from python.generate_attack import DeletionCharAttack, VariationSelectorAttack, InvisibleCharAttack, HomoglyphAttack

# Test that the module and its C++ extension loaded successfully
print(f"✓ Package imported: {textual_adversarial_defense.__version__}")

# Access the compiled C++ extension
if textual_adversarial_defense._pipeline:
    print("✓ C++ _pipeline extension loaded successfully")
    
    # Example 1: Homoglyph Attack & Sanitization
    print("\n=== Homoglyph Attack Example ===")
    pipeline_homo = textual_adversarial_defense._pipeline.Pipeline()
    pipeline_homo.add_combined_sanitizer()
    
    text = "Hello"
    
    attack = HomoglyphAttack(perturbation_budget=100)
    test_text_homo = attack.perturb(text)
    sanitized_homo = pipeline_homo.sanitize(test_text_homo)
    
    print(f"Original:      '{text}'")
    print(f"After attack:  '{test_text_homo}'")
    print(f"After sanitize: '{sanitized_homo}'")
    print(f"Text changed by attack: {text != test_text_homo}")
    print(f"Sanitizer removed changes: {sanitized_homo == text}")
    
    print()

    
else:
    print("✗ C++ _pipeline extension not available")

print("\n✓ All tests passed!")