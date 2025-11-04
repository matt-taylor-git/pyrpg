#!/usr/bin/env python3
"""Regenerate monster sprites with scary, menacing appearance facing left."""

import os
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
import io
from rembg import remove

# Configure API
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# Monster definitions with scary descriptions
MONSTERS = {
    "goblin": "A menacing, scary goblin monster with sharp teeth and claws, snarling aggressively, facing left, dark fantasy RPG game sprite, detailed hand-drawn illustration style, threatening posture, side view",
    "orc": "A terrifying, massive orc warrior with brutal features and fierce expression, wielding a weapon, facing left, dark fantasy RPG game sprite, menacing and intimidating, detailed illustration, profile view",
    "golem": "A fearsome stone golem with glowing angry eyes, massive intimidating form, cracked rocky texture, facing left, dark fantasy RPG game sprite, threatening and powerful, side angle",
    "skeleton": "A horrifying undead skeleton warrior with glowing eyes in empty sockets, wielding ancient weapons, facing left, dark fantasy RPG game sprite, menacing and ghostly, tattered armor, side profile",
    "bandit": "A dangerous, sinister bandit with scarred face and cruel expression, holding weapons, facing left, dark fantasy RPG game sprite, threatening outlaw, dark clothing, looking left",
    "wolf": "A ferocious, snarling dire wolf with bared fangs and glowing predatory eyes, aggressive stance, facing left, dark fantasy RPG game sprite, menacing beast, side view profile",
    "spider": "A horrifying giant spider with venomous fangs, multiple glowing eyes, threatening pose, facing left, dark fantasy RPG game sprite, creepy and dangerous, side angle view",
    "slime": "A menacing toxic slime creature with acidic bubbling surface and sinister form, facing left, dark fantasy RPG game sprite, dangerous ooze monster, side profile",
    "boss": "An intimidating shadow lord boss with dark armor, glowing red eyes, commanding presence, facing left, dark fantasy RPG game sprite, powerful and menacing elite enemy, side view",
    "final_boss": "A terrifying dark overlord final boss with massive imposing form, demonic features, glowing eyes, dark energy aura, facing left, dark fantasy RPG game sprite, ultimate evil threat, side profile"
}

def generate_monster_sprite(name: str, prompt: str, output_path: Path):
    """Generate a single monster sprite."""
    print(f"\n{'='*60}")
    print(f"Generating: {name}")
    print(f"Prompt: {prompt}")
    print(f"{'='*60}")

    try:
        # Generate image using Imagen 3
        config = types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
        )

        result = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=prompt,
            config=config,
        )

        if not result.generated_images:
            print(f"❌ No images generated for {name}")
            return False

        # Get the image
        image_bytes = result.generated_images[0].image.image_bytes
        print(f"✓ Generated image: {len(image_bytes)} bytes")

        # Remove background
        print("  Removing background...")
        image = Image.open(io.BytesIO(image_bytes))
        output_image = remove(image)

        # Save
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_image.save(output_path, "PNG")
        print(f"✓ Saved to: {output_path}")

        return True

    except Exception as e:
        print(f"❌ Failed to generate {name}: {e}")
        return False

def main():
    """Generate all monster sprites."""
    project_root = Path(__file__).parent
    assets_dir = project_root / "assets"

    print("="*60)
    print("Monster Sprite Regeneration")
    print("Generating scary, menacing sprites facing left")
    print("="*60)

    success_count = 0
    failed = []

    for name, prompt in MONSTERS.items():
        output_path = assets_dir / f"{name}.png"
        if generate_monster_sprite(name, prompt, output_path):
            success_count += 1
        else:
            failed.append(name)

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✓ Successfully generated: {success_count}/{len(MONSTERS)}")
    if failed:
        print(f"❌ Failed: {', '.join(failed)}")
    print("="*60)

if __name__ == "__main__":
    main()
