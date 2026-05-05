from PIL import Image
import os

def transform_pixels(image, func):
    pixels = list(image.getdata())
    mode = image.mode

    new_pixels = []
    for pixel in pixels:
        if mode == 'RGBA':
            r, g, b, a = pixel
            nr, ng, nb = func(r, g, b)
            new_pixels.append((nr, ng, nb, a))
        else:
            r, g, b = pixel
            new_pixels.append(func(r, g, b))

    result = Image.new(mode, image.size)
    result.putdata(new_pixels)
    return result


def xor_pixels(image, key):
    return transform_pixels(image, lambda r, g, b: (r ^ key, g ^ key, b ^ key))


def add_key_pixels(image, key):
    return transform_pixels(image, lambda r, g, b: ((r + key) % 256, (g + key) % 256, (b + key) % 256))


def subtract_key_pixels(image, key):
    return transform_pixels(image, lambda r, g, b: ((r - key) % 256, (g - key) % 256, (b - key) % 256))


def swap_pixels(image):
    pixels = list(image.getdata())
    mode = image.mode

    new_pixels = pixels[:]

    for i in range(0, len(pixels) - 1, 2):
        new_pixels[i], new_pixels[i + 1] = pixels[i + 1], pixels[i]

    if len(pixels) % 2 != 0:
        print("  Note: Last pixel unchanged due to odd pixel count.")

    result = Image.new(mode, image.size)
    result.putdata(new_pixels)
    return result


def load_image(path):
    try:
        img = Image.open(path)
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')
        print(f"  Loaded: {path} | Size: {img.size} | Mode: {img.mode}")
        return img
    except FileNotFoundError:
        print(f"  ERROR: File not found — '{path}'")
        return None
    except Exception as e:
        print(f"  ERROR loading image: {e}")
        return None


def save_image(image, path):
    try:
        image.save(path)
        print(f"  Saved: {path}")
    except Exception as e:
        print(f"  ERROR saving image: {e}")


def get_key(prompt="Enter key (0–255): "):
    while True:
        try:
            key = int(input(prompt))
            if 0 <= key <= 255:
                return key
            else:
                print("  Key must be between 0 and 255.")
        except ValueError:
            print("  Invalid input. Enter a number.")


def build_output_path(original_path, suffix):
    base, _ = os.path.splitext(original_path)
    return f"{base}_{suffix}.png"


def main():
    print("=" * 50)
    print("        IMAGE ENCRYPTION TOOL")
    print("=" * 50)

    image_path = input("\nEnter image path: ").strip()
    image = load_image(image_path)

    if image is None:
        return

    original_image = image.copy()

    while True:
        print("\n── Operations ──────────────────────────")
        print("  1. Encrypt with XOR")
        print("  2. Decrypt with XOR")
        print("  3. Encrypt with pixel addition")
        print("  4. Decrypt with pixel subtraction")
        print("  5. Swap adjacent pixels")
        print("  6. Reset to original image")
        print("  7. Load new image")
        print("  8. Exit")
        print("────────────────────────────────────────")

        choice = input("Choose option (1–8): ").strip()

        if choice == "1":
            key = get_key()
            result = xor_pixels(image, key)
            out = build_output_path(image_path, "xor_encrypted")

        elif choice == "2":
            key = get_key()
            result = xor_pixels(image, key)
            out = build_output_path(image_path, "xor_decrypted")

        elif choice == "3":
            key = get_key()
            result = add_key_pixels(image, key)
            out = build_output_path(image_path, "add_encrypted")

        elif choice == "4":
            key = get_key()
            result = subtract_key_pixels(image, key)
            out = build_output_path(image_path, "sub_decrypted")

        elif choice == "5":
            result = swap_pixels(image)
            out = build_output_path(image_path, "swapped")

        elif choice == "6":
            image = original_image.copy()
            print("  Image reset to original.")
            continue

        elif choice == "7":
            new_path = input("Enter new image path: ").strip()
            new_image = load_image(new_path)
            if new_image:
                image = new_image
                original_image = new_image.copy()
                image_path = new_path
            continue

        elif choice == "8":
            print("\nGoodbye!")
            break

        else:
            print("  Invalid choice.")
            continue

        save_image(result, out)
        image = result
        image_path = out


if __name__ == "__main__":
    main()