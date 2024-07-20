document.getElementById('ats-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const scanButton = event.target.querySelector('button[type="submit"]');
    scanButton.disabled = true;
    scanButton.innerText = 'Scanning...';

    const formData = new FormData();
    formData.append('resume', document.getElementById('resume').files[0]);
    formData.append('jobDescription', document.getElementById('job-description').value);

    const response = await fetch('/scan', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const result = await response.json();
        document.getElementById('percentage-match').innerText = `ATS Score: ${result.percentageMatch}%`;
        document.getElementById('resume-skills').innerText = `Resume Skills: ${result.resumeSkills.join('\n')}`;
        document.getElementById('job-description-skills').innerText = `Job Description Skills: ${result.jobDescriptionSkills.join('\n')}`;
        document.getElementById('lacking-skills').innerText = `Lacking Skills: ${result.lackingSkills.join('\n')}`;
        document.getElementById('extra-skills').innerText = `Extra Skills: ${result.extraSkills.join('\n')}`;
        document.getElementById('matched-skills').innerText = `Matched Skills: ${result.matchedSkills.join('\n')}`;
        document.getElementById('results').classList.remove('hidden');
    } else {
        alert('Failed to scan resume.');
    }

    scanButton.disabled = false;
    scanButton.innerText = 'Scan';
});

document.getElementById('resume').addEventListener('change', (event) => {
    const fileLabel = document.getElementById('file-label');
    const pdfIcon = document.getElementById('pdf-icon');
    const file = event.target.files[0];

    if (file && file.type === 'application/pdf') {
        fileLabel.innerText = file.name;
        pdfIcon.classList.remove('hidden');
    } else {
        fileLabel.innerText = 'Choose file';
        pdfIcon.classList.add('hidden');
    }
});
