#!/bin/bash
# Build ClaimEdge .skill packages from source directories
# Usage: ./build-skills.sh [output_dir]

set -e

OUTPUT_DIR="${1:-./built}"
mkdir -p "$OUTPUT_DIR"

echo "=========================================="
echo "ClaimEdge Skill Package Builder"
echo "=========================================="
echo ""

for skill_dir in claimedge-*/; do
    if [ -d "$skill_dir" ]; then
        skill_name="$(basename "$skill_dir")"
        output_file="$OUTPUT_DIR/${skill_name}.skill"
        
        echo "Building: $skill_name"
        
        # Create ZIP archive with .skill extension
        (cd "$skill_dir" && zip -r "../$output_file" . -x "*.DS_Store" -x "*__pycache__*" -x "*.pyc")
        
        # Get file size
        size=$(du -h "$output_file" | cut -f1)
        echo "  → $output_file ($size)"
        echo ""
    fi
done

echo "=========================================="
echo "Build complete! Packages in: $OUTPUT_DIR/"
echo "=========================================="
ls -lh "$OUTPUT_DIR/"/*.skill 2>/dev/null || echo "No .skill files found"
