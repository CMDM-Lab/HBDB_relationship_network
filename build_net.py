import os
import json
import mysql.connector

connection = mysql.connector.connect(host='localhost',
                                      port='3306',
                                      user='root',
                                      password='XXXXXXXX')

cursor = connection.cursor()
cursor.execute("USE `hbdb2`;")

base_path = "./score_extract"
output_path = "./network"

# Metadata categories
metadata_categories = [
    'concept_abnormality_metadata', 
    'concept_chemical_metadata', 
    'concept_molecular function_metadata', 
    'concept_gene_metadata', 
    'concept_location_metadata', 
    'concept_animal model_metadata'
]

for sub_dir in os.listdir(base_path):
    sub_dir_path = os.path.join(base_path, sub_dir)
    
    if os.path.isdir(sub_dir_path):
        # Extract term from sub_dir_path
        term = sub_dir_path.split("/")[-1].split("_", 1)[-1]

        all_networks = {} 

        compound_network = {"nodes": [], "edges": []}
        compound_network["nodes"].append({
            "data": {
                "id": term,
                "label": term,
                "type": "compound",
            }
        })

        # Term to metadata layer
        for metadata in metadata_categories:
            compound_network["nodes"].append({
                "data": {
                    "id": metadata,
                    "label": metadata.split("_")[1],
                    "type": "metadata",
                }
            })
            compound_network["edges"].append({
                "data": {
                    "type": "compound_to_metadata",
                    "source": term,
                    "target": metadata,
                    "score": None
                }
            })

        # Metadata to concepts layer
        metadata_networks = {}
        for metadata in metadata_categories:
            metadata_network = {"nodes": [], "edges": []}
            metadata_network["nodes"].append({
                "data": {
                    "id": term,
                    "label": term,
                    "type": "compound",
                }
            })

            metadata_path = os.path.join(sub_dir_path, metadata)
            for concept in os.listdir(metadata_path):
                concept_path = os.path.join(metadata_path, concept)
                if os.path.isdir(concept_path):
                    total_score = 0

                    for paper_id in os.listdir(concept_path):
                        paper_path = os.path.join(concept_path, paper_id)
                        if os.path.isdir(paper_path):
                            for file in os.listdir(paper_path):
                                file_path = os.path.join(paper_path, file)
                                with open(file_path, "r", encoding="utf-8") as f:
                                    content = json.load(f)
                                    total_score += content.get("score", 0)

                    metadata_network["nodes"].append({
                        "data": {
                            "id": concept,
                            "label": concept,
                            "type": "concept",
                        }
                    })
                    metadata_network["edges"].append({
                        "data": {
                            "type": "compound_to_concept",
                            "source": term,
                            "target": concept,
                            "score": total_score
                        }
                    })

            metadata_networks[metadata] = metadata_network

        # Concept to papers and summaries layer
        concept_networks = {}
        for metadata in metadata_categories:
            metadata_path = os.path.join(sub_dir_path, metadata)
            for concept in os.listdir(metadata_path):
                concept_path = os.path.join(metadata_path, concept)
                if os.path.isdir(concept_path):
                    concept_network = {"nodes": [], "edges": []}
                    concept_network["nodes"].append({
                        "data": {
                            "id": concept,
                            "label": concept,
                            "type": "concept",
                        }
                    })

                    for paper_id in os.listdir(concept_path):
                        cursor.execute(f"SELECT * FROM `references` WHERE `id` = {paper_id};")
                        ret = cursor.fetchall()[0]
                        pmid = str(ret[7])
                        paper_link = "https://pubmed.ncbi.nlm.nih.gov/" + pmid
                        title = ret[1]
                        author = ret[2]
                        citation = ret[3]

                        paper_path = os.path.join(concept_path, paper_id)
                        if os.path.isdir(paper_path):
                            concept_network["nodes"].append({
                                "data": {
                                    "id": paper_id,
                                    "label": f"{title}\n{author}\n{citation}",
                                    "type": "paper",
                                    "url": paper_link,
                                }
                            })
                            concept_network["edges"].append({
                                "data": {
                                    "type": "concept_to_paper",
                                    "source": concept,
                                    "target": paper_id,
                                    "score": None
                                }
                            })

                            for file in os.listdir(paper_path):
                                file_path = os.path.join(paper_path, file)
                                with open(file_path, "r", encoding="utf-8") as f:
                                    content = json.load(f)
                                    now_score = content.get("score", 0)
                                    summary_id = f"{paper_id}_{file}"
                                    concept_network["nodes"].append({
                                        "data": {
                                            "id": summary_id,
                                            "label": content.get("summary", "No summary"),
                                            "type": "summary",
                                        }
                                    })
                                    concept_network["edges"].append({
                                        "data": {
                                            "type": "paper_to_summary",
                                            "source": paper_id,
                                            "target": summary_id,
                                            "score": now_score
                                        }
                                    })

                    concept_networks[concept] = concept_network

        output_data = {
            "compound_network": compound_network,
            "metadata_networks": metadata_networks,
            "concept_networks": concept_networks
        }

        # Get original file name from all_results/
        original_file_name = sub_dir.split("_", 1)[0] + "_" + sub_dir.split("_", 1)[-1] + ".json"
        output_file_path = os.path.join(output_path, original_file_name)

        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

        print(f"Network data saved to {output_file_path}")

print("All data processing complete.")
