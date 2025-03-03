Steps

1. Generate Scores and Summaries

Use GPT-4 to generate the required scores and summaries:
```bash
python gen_scores.py
```
2. Process Generated Data

Extract and process the generated data:
```bash
python extract.py
```
3. Generate Node and Edge Format for Cytoscape

Build the network structure in the required format:
```bash
python build_net.py
```
4. Display Network

Install dependencies and run the server:
```bash
npm install express
node server.js
```
5. View the Network
the url of each network: http://localhost:8001/index.html?file={com}_acetone
Open the following URL in your browser:
```bash
http://localhost:8001/index.html?file=28_acetone
```