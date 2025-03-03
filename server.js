const express = require('express');
const path = require('path');

const app = express();
const PORT = 8001;

app.use(express.static(path.join(__dirname, 'public')));

app.get('/:file.json', (req, res) => {
    const fileName = req.params.file;
    const filePath = path.join(__dirname, 'network', `${fileName}.json`);

    res.sendFile(filePath, (err) => {
        if (err) {
            console.error(`Error loading file: ${filePath}`, err);
            res.status(404).send('File not found');
        }
    });
});

// url: http://localhost:8001/index.html?file=13_3-Nitrotyrosine
// url: http://localhost:8001/index.html?file=28_acetone
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
