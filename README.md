# hbdb codes

## Data Requirements
Download the `hbdb2.sql` and put it in the same directory

## Environment Setup
Create a new conda environment
```bash
conda create --name hbdb_env python=3.10
```
Activate the conda environment
```bash
conda activate hbdb_env
```
Install necessary package
```bash
pip insall mysql-connector-python==9.1.0
pip install openai==1.63.0
```

## Modify `gen_scores.py` and  `build_net.py` to match your dataset format
Replace the following line in the script with your own MySQL settings:
```bash
connection = mysql.connector.connect(host='localhost', port='3306',user='root'password='XXXXXXXX')
```
Ensure the host, port, user, and password match your database configuration.

- host: The hostname or IP address of your MySQL server.
- port: The port number your MySQL server listens on (default is 3306).
- user: Your MySQL username.
- password: Your MySQL password (replace XXXXXXXX with the actual password).

## Set your OPENAI_API_KEY in `prompt.py`
```bash
os.environ["OPENAI_API_KEY"] = "Your API KEY"
```

## Build Network Steps
### 1. Use gpt-4o-mini to generate scores and summaries:
```bash
python gen_scores.py
```
### 2. Process the generated data:
```bash
python extract.py
```
### 3. Build the network structure in the Cytoscape format:
```bash
python build_net.py
```
### 4. Run the server to diaplay network
```bash
npm install express
node server.js
```
### 5. View the network
The URL format is `http://localhost:8001/index.html?file={compound_id}_{compound_name}`
Take acetone for example, you can open the following URL in your browser to view its network:
```bash
http://localhost:8001/index.html?file=28_acetone
``` 
## Evaluation Steps
### Prepare Dataset
download `BC8_BioRED_Subtask1_BioCJSON/bc8_biored_task1_train.json` and put it in the same directory

### Run Evaluation
```bash
python eval.py
```
