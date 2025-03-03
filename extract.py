import os
import json
import re
from collections import defaultdict

source_dir = './all_results'
output_dir = './score_extract'

metadata_categories = ['concept_abnormality_metadata', 'concept_chemical_metadata', 'concept_molecular function_metadata', 'concept_gene_metadata', 'concept_location_metadata', 'concept_animal model_metadata']

for sub_dir in os.listdir(source_dir):
    sub_dir_path = os.path.join(source_dir, sub_dir)
    
    if os.path.isdir(sub_dir_path):
        output_sub_dir = os.path.join(output_dir, sub_dir)
        
        if not os.path.exists(output_sub_dir):
            os.makedirs(output_sub_dir)

        # Step 1: Collect concepts for each metadata category
        metadata_concepts = {key: set() for key in metadata_categories}

        for category in metadata_categories:
            category_path = os.path.join(sub_dir_path, category)

            if not os.path.exists(category_path):
                print(f"Skipping missing category folder: {category} in {sub_dir}")
                continue

            for compound_dir in os.listdir(category_path):
                compound_path = os.path.join(category_path, compound_dir)

                if os.path.isdir(compound_path):
                    for filename in os.listdir(compound_path):
                        parts = filename.split("_")
                        if len(parts) > 1:  # Ensure there is a concept part
                            concept = parts[1]
                            metadata_concepts[category].add(concept)

        for category, concepts in metadata_concepts.items():
            concepts_list = sorted(concepts)
            print(f"{category} concepts in {sub_dir}:")
            print(concepts_list)
            print("\n")

        # Step 2: Restructure files into concept-based directories
        for category, concepts in metadata_concepts.items():
            category_path = os.path.join(sub_dir_path, category)

            if not os.path.exists(category_path):
                print(f"Skipping missing category folder: {category} in {sub_dir}")
                continue

            target_category_path = os.path.join(output_sub_dir, category)

            if not os.path.exists(target_category_path):
                os.makedirs(target_category_path)

            for concept in concepts:
                concept_dir = os.path.join(target_category_path, concept)
                if not os.path.exists(concept_dir):
                    os.makedirs(concept_dir)

            for compound_dir in os.listdir(category_path):
                compound_path = os.path.join(category_path, compound_dir)

                if os.path.isdir(compound_path):
                    for filename in os.listdir(compound_path):
                        parts = filename.split("_")
                        if len(parts) > 1:
                            concept = parts[1]
                            paper_id = compound_dir

                            paper_dir = os.path.join(target_category_path, concept, paper_id)
                            if not os.path.exists(paper_dir):
                                os.makedirs(paper_dir)

                            file_path = os.path.join(compound_path, filename)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = json.load(f)
                                summary = content.get("llm_generation", {}).get("summary", "No summary provided")
                                score = content.get("llm_generation", {}).get("score", 0)

                                output_data = {
                                    "paper_id": paper_id,
                                    "score": score,
                                    "summary": summary
                                }

                                output_file_path = os.path.join(paper_dir, filename)
                                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                                    json.dump(output_data, output_file, ensure_ascii=False, indent=4)

        print(f"Data restructuring complete for {sub_dir}. Results stored in: {output_sub_dir}")

print("All data restructuring complete.")
