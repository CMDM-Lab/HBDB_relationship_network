import os
import json
from prompt import get_relationship_summary_and_score

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def process_dataset(json_filepath, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    data = load_json(json_filepath)
    documents = data.get("documents", [])

    idx = 1  
    for doc in documents:
        doc_id = doc["id"]  # ex: BC8_BioRED_Task1_Doc0
        context = ""
        terms = {}  
        annotations = {} 
        #if(idx > 3):
        #    break
        for passage in doc.get("passages", []):
            passage_type = passage["infons"].get("type", "")
            if passage_type == "abstract":
                context = passage["text"]
            elif passage_type in ["title", "abstract"]:
                for annotation in passage.get("annotations", []):
                    annotation_id = annotation["id"]
                    term_text = annotation["text"]
                    annotations[annotation_id] = term_text

        for relation in doc.get("relations", []):
            entity1 = relation["infons"]["entity1"]
            entity2 = relation["infons"]["entity2"]
            relation_type = relation["infons"]["type"]

            term_A = None
            term_B = None

            for passage in doc.get("passages", []):
              for annotation in passage.get("annotations", []):
                if annotation["infons"].get("identifier") == entity1:
                  term_A = annotation["text"]
                if annotation["infons"].get("identifier") == entity2:
                  term_B = annotation["text"]

            term_A = term_A if term_A else f"Unknown({entity1})"
            term_B = term_B if term_B else f"Unknown({entity2})"

            # clean
            term_A = term_A.replace("/", "_").replace("\\", "_")
            term_B = term_B.replace("/", "_").replace("\\", "_")

            # print(idx)
            llm_result = get_relationship_summary_and_score(context, term_A, term_B)

            if isinstance(llm_result, str):
                llm_result = json.loads(llm_result)

            result = {
                "term_A": term_A,
                "term_B": term_B,
                "context": context,
                "relation_type": relation_type,
                "summary": llm_result.get("summary", ""),
                "reason": llm_result.get("reason", ""),
                "llm_score": int(llm_result.get("score", 0))
            }

            # format: idx_DocX_termA_termB_relation.json
            result_filename = f"{idx}_{doc_id.split('_')[-1]}_{term_A}_{term_B}_{relation_type}.json"
            save_json(os.path.join(output_dir, result_filename), result)
            idx += 1

    print(f"Processed {idx} relations and saved results to {output_dir}.")

if __name__ == "__main__":
    dataset_path = "./BC8_BioRED_Subtask1_BioCJSON/bc8_biored_task1_train.json"
    output_directory = "eval_results"
    process_dataset(dataset_path, output_directory)
