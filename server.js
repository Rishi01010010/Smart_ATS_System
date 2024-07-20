const express = require('express');
const multer = require('multer');
const path = require('path');
const { PythonShell } = require('python-shell');

const app = express();
const port = process.env.PORT || 3000;

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        cb(null, `${Date.now()}-${file.originalname}`);
    }
});

const upload = multer({ storage: storage });

app.use(express.static('public'));

app.post('/scan', upload.single('resume'), (req, res) => {
    const jobDescription = req.body.jobDescription;
    const resumePath = req.file.path;

    const options = {
        mode: 'text',
        pythonOptions: ['-u'],
        args: [resumePath, jobDescription]
    };

    PythonShell.run('ats.py', options, (err, results) => {
        if (err) {
            console.error(err);
            return res.status(500).send('Error processing resume');
        }

        const [resumeSkills, jobDescriptionSkills, lackingSkills, extraSkills, matchedSkills, percentageMatch] = results.map(result => JSON.parse(result));
        res.json({
            resumeSkills,
            jobDescriptionSkills,
            lackingSkills,
            extraSkills,
            matchedSkills,
            percentageMatch
        });
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
