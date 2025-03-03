import os
import json
import mysql.connector
import time

start_time = time.time()

from prompt import get_relationship_summary_and_score
connection = mysql.connector.connect(host='localhost',
                                    port='3306',
                                    user='root',
                                    password='XXXXXXXX')

cursor = connection.cursor()
cursor.execute("USE `hbdb2`;")

tables_dir_name = ['concept_abnormality_metadata', 'concept_chemical_metadata', 'concept_molecular function_metadata', 'concept_gene_metadata', 'concept_location_metadata', 'concept_animal model_metadata']
tables = ['concept_abnorm_metadata', 'concept_chemical_metadata', 'concept_function_metadata', 'concept_gene_metadata', 'concept_location_metadata', 'concept_model_metadata']

# compound_id = 28

# all compound: 1 to 1052
for compound_id in range(1, 1052):
    print(f"compound_id = {compound_id}\n")
    
    for idx, table in enumerate(tables):
        print(f"idx = {idx}\n")
        print(table)
        cursor.execute(f"SELECT * FROM {table} WHERE `compound_id`={compound_id} AND `is_related`=1;")
        ret = cursor.fetchall()
        cursor.execute(f"SELECT `name` FROM `compounds` WHERE `id`={compound_id};")

        compound_data = cursor.fetchall()
        if compound_data == []:
            print("can't find compound name\n")
            continue
        term_a = compound_data[0][0]
        for i in ret:
            concept_id = i[2]
            if table == 'concept_abnorm_metadata':
                reference_id = i[7] 
                paragraph = i[5]
                sentance = i[6]
            else:
                reference_id = i[3] 
                paragraph = i[6]
                sentance = i[7]

            
            if paragraph is not None and len(paragraph) > 20:
                paragraph = paragraph[:20]
            else:
                paragraph = paragraph or ""

            print(f"concept id = {concept_id}\n")
            cursor.execute(f"SELECT `concept_name` FROM `concepts` WHERE `id`={concept_id};")
            concept_data = cursor.fetchall()
            # print(concept_data)
            if concept_data == []:
                print("can't find concept name\n")
                continue
            term_b = concept_data[0][0]
            print(f"now in {table}\n{compound_id}\n{concept_id}\n{reference_id}\n\n")

            query = """
                SELECT *
                FROM `sentences`
                WHERE `content` LIKE %s AND `reference_id` = %s;
            """
            cursor.execute(query, (sentance, reference_id))
            k = cursor.fetchall()
            
            if k == []:
                print("No results found\n")
            start_idx = k[0][0] - 3
            end_idx = k[0][0] + 3
            
            cursor.execute(f"SELECT `content` FROM `sentences` WHERE `id` BETWEEN {start_idx} AND {end_idx};")
            kk = cursor.fetchall()
            context=""
            for j in kk:
                context += j[0] + ' '
            # print(f"word_a = {word_a}\nword_b = {word_b}\ncontext = {context}\n")

            # generate summary
            llm_response = get_relationship_summary_and_score(context, term_a, term_b)
            parsed_response = json.loads(llm_response)

            response_with_context = {
                "context": context,
                "term_A": term_a,
                "term_B": term_b,
                "llm_generation": parsed_response,
            }

            # initialize 6 tables
            for table_name in tables_dir_name:
                save_path = f"./all_results/{compound_id}_{term_a}/{table_name}/"
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

            save_path = f"./all_results/{compound_id}_{term_a}/{tables_dir_name[idx]}/{reference_id}/{term_a}_{term_b}_{paragraph}.json"
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "w") as file:
                json.dump(response_with_context, file, indent=4)

        # print(llm_response)

cursor.close()
connection.close()

end_time = time.time()
execution_time = end_time - start_time

print(f"Results saved to {save_path}")
print(f"Total execution time: {execution_time:.2f} seconds")