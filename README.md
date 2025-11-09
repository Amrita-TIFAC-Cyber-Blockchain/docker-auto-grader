# Docker Auto-Grader using GitHub Actions

This repository automates the testing and grading of student-submitted Docker images using GitHub Actions.
All grading runs remotely — no need for Docker Desktop or Docker Engine on your local machine.

### Ideal for:
🎓 Academic courses where students submit Dockerized projects. <br/> 
🧑‍🏫 Teaching assistants automating grading or validation. <br/> 
🧰 Verifying Docker images at scale in a secure environment. <br/> 

### Features

✅ Automated Execution — Pulls and tests each Docker Hub image remotely using GitHub-hosted runners. <br/> 
✅ Custom Test Logic — You can define your own grading logic in tests/test_script.py. <br/> 
✅ Detailed Logs & Reports — Generates individual logs and a summary CSV with pass/fail results. <br/> 
✅ No Local Setup Required — Runs entirely in GitHub Actions (Docker preinstalled). <br/> 
✅ Sandboxed Containers — Prevents untrusted images from accessing the internet. <br/> 
