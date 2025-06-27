import json
import sys
import os

def add_prefix_to_openapi_paths(spec_filepath, prefix="/api/v1/", output_filepath=None):
    """
    Adds a specified prefix to all paths in an OpenAPI v3.0 JSON specification file.

    Args:
        spec_filepath (str): The path to the original OpenAPI JSON specification file.
        prefix (str): The prefix string to add to each path.
        output_filepath (str, optional): The path to save the modified spec.
                                        If None, the original file will be overwritten.
    """
    if not os.path.exists(spec_filepath):
        print(f"Error: Specification file not found at '{spec_filepath}'.")
        sys.exit(1)

    try:
        with open(spec_filepath, 'r') as f:
            spec = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON from '{spec_filepath}'. Details: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error: Could not open or read file '{spec_filepath}'. Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while loading the spec: {e}")
        sys.exit(1)

    if "paths" in spec and isinstance(spec["paths"], dict):
        original_paths = spec["paths"]
        modified_paths = {}
        print("\n--- Modifying paths ---")
        for path, path_item in original_paths.items():
            new_path = prefix + path.lstrip('/') # Ensure no double slashes if path starts with '/'
            modified_paths[new_path] = path_item
            print(f"  Original: {path} -> Modified: {new_path}")
        spec["paths"] = modified_paths
    else:
        print("No 'paths' found in the OpenAPI specification or it's not a dictionary. No modifications made.")
        # We don't exit here, as the user might still want to save the original file if no paths were found.

    # Determine the output file path
    if output_filepath:
        target_filepath = output_filepath
    else:
        target_filepath = spec_filepath

    try:
        # Write the modified spec back to the file
        # Using indent for pretty-printing the JSON
        with open(target_filepath, 'w') as f:
            json.dump(spec, f, indent=2)
        print(f"\nSuccessfully wrote modified spec to: {target_filepath}")
    except IOError as e:
        print(f"Error: Could not write modified spec to '{target_filepath}'. Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while writing the spec: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Define the path to your OpenAPI spec file
    spec_file = r'/mnt/c/OPENAPI_MCP/hf_spec.json' # CHANGE THIS to your actual file path

    # Define the output file path (optional).
    # If None, the original file will be overwritten.
    # To create a copy, uncomment and set a different path:
    output_file = r'/mnt/c/OPENAPI_MCP/hf_spec_modified.json'
    # output_file = None # Uncomment this line to overwrite the original file

    # Define the prefix you want to add
    path_prefix = "/api/v1/"

    print(f"Attempting to modify paths in: {spec_file}")
    if output_file:
        print(f"Saving modified spec to: {output_file}")
    else:
        print("WARNING: Original file will be overwritten!")

    add_prefix_to_openapi_paths(spec_file, prefix=path_prefix, output_filepath=output_file)

    print("\nModification complete.")
