"""
Script to patch Streamlit's internal iframe policy list to remove unsupported features.

Usage:
    python scripts/patch_streamlit_iframe_policy.py

Description:
    Streamlit 1.x includes a hardcoded list of Feature Policy directives (accelerometer, gyroscope, etc.)
    in its frontend code (IFrameUtil main bundle). Many of these are deprecated or renamed in modern browsers,
    causing console warnings like 'Feature Policy: Skipping unsupported feature name "vr"'.
    
    This script locates the installed Streamlit package, finds the specific JS file containing the list,
    and replaces it with a minimal "safe" list (camera, microphone, etc.) to silence the warnings.
    
    Run this script after installing or upgrading Streamlit if the warnings reappear.
"""
import os
import glob
import re
import sys

def patch_streamlit_iframe_policy(dry_run=False):
    try:
        import streamlit
    except ImportError:
        print("Error: Streamlit not found. Please run in the correct virtual environment.")
        return

    # 1. Locate the file(s)
    streamlit_path = os.path.dirname(streamlit.__file__)
    js_dir = os.path.join(streamlit_path, "static", "static", "js")
    
    # We want to check ALL .js files because the list might be inlined in the main bundle (index.*.js)
    # or exist in a utility file (IFrameUtil.*.js).
    js_files = glob.glob(os.path.join(js_dir, "*.js"))
    
    if not js_files:
        print(f"Error: No JS files found in {js_dir}")
        return

    print(f"Scanning {len(js_files)} JS files in {js_dir}...")

    # 2. Define the replacement logic
    # Safe list (features that generally don't warn):
    safe_features = [
        "camera",
        "fullscreen",
        "geolocation",
        "microphone",
        "publickey-credentials-get"
    ]
    
    formatted_safe_list = ",".join(f'"{f}"' for f in safe_features)
    replacement_code = f'o=[{formatted_safe_list}].join("; ")'
    
    # Regex to find the list. 
    # The minified code usually looks like: const o=["accelerometer",...,"gyroscope",...].join("; ")
    # or: o=["accelerometer",...,"gyroscope",...].join("; ")
    # We look for a bracketed list containing "gyroscope" followed explicitly by .join("; ")
    pattern = r'(\w+)=\[[^\]]*"gyroscope"[^\]]*\]\.join\("; "\)'

    patched_count = 0

    for file_path in js_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if file has the target string
        if "gyroscope" not in content:
            continue

        print(f"Found keyword 'gyroscope' in: {os.path.basename(file_path)}")
        
        match = re.search(pattern, content)
        if not match:
             # Try slightly different pattern for const declarations if needed, 
             # but usually variable assignment is what we see.
             # fallback: try just the list part if variable assignment name varies too much
             # pattern_lazy = r'\[[^\]]*"gyroscope"[^\]]*\]\.join\("; "\)'
             print(f"  Warning: Regex failed to match strict pattern in {os.path.basename(file_path)}")
             continue

        if dry_run:
            print(f"  [Dry Run] Would patch {os.path.basename(file_path)}")
            continue

        # Use a function for replacement to keep the variable name found in the group
        # match.group(0) is the whole string: o=["...","gyroscope"...].join("; ")
        # match.group(1) is the variable name: o
        var_name = match.group(1)
        # We construct the exact replacement keeping the variable name
        full_replacement = f'{var_name}=[{formatted_safe_list}].join("; ")'
        
        new_content = re.sub(pattern, full_replacement, content)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print(f"  Success: Patched {os.path.basename(file_path)}")
        patched_count += 1

    if patched_count == 0:
        print("Warning: No files were patched. Feature list not found or already patched.")
    else:
        print(f"Total files patched: {patched_count}")
        print("Please restart Streamlit (Ctrl+C, then run again) and CLEAR BROWSER CACHE.")

if __name__ == "__main__":
    patch_streamlit_iframe_policy()
