# SkillSyncer
This is SkillSyncer! An AI based tool which streamlines resume matching. You can consider it your AI HR assistant, automating project matching with employees. 

We have fully integrated database support, account support and multi project / employee support. Simply create an account and upload the PDF resumes of your employees, and a text description of the projects your company aims to work on. The rest will be handled by the AI!

For more informmation, visit our [final presentation slides](https://docs.google.com/presentation/d/114gSoesFxxMDDUXXutnhAdf1lSK36WeHCBM_zN_RKFI/edit#slide=id.g2c299bb166e_0_0)

# Get Started:
1. ```pip install -r requirements.txt```
2. ```export OPENAI_API_KEY={your_api_key}```
3. ```python3 app.py```


# Team Member's Contributions
## Sprint 1
1. Krrish Chawla
What I did: Built Front End + Back End, OpenAI Integration, Prompting
What I aim to do for next sprint: Work on better matching models and data masking or encryption, more front/backend

2. Arvind Saligrama
What I did: Researched embedding models and decided to use INSTRUCTOR embeddings. Created prompts for INSTRUCTOR model and implemented similarity matching algorithm for app.
What I aim to do for next sprint: Try and improve matching/embedding models. Work on more backend. User interviews for features to add.

3. Roy Yuan
What I did: did brute force method for matching, collected resumes, prompting, brainstorm encryption and algorithm
What I aim to do for next sprint: Integrate better brute force method with app, more backend, work on encryption


## Sprint 2
1. Krrish Chawla
What I did: Experimented with different algorithms for matching, built more frontend, created a few data masking pipelines and finalized on the one that uses LLMs.
What I aim to do for next sprint: Incorporate data masking, finalize on matching algorithm, make back-end more efficient, more front end (we aim to include a button to generate matches on demand)

2. Arvind Saligrama
What I did: Wrote algorithm that updates best employee for each project whenever you upload a new employee. Integrated brute force algorithm with current embeddindgs algorithm. Did a user interview
What I aim to do for next sprint: Work on getting better embeddings. Specifically, a chunking algorithm that assigns weights to different experiences on the resume.

3. Roy Yuan
What I did: finished brute force algorithm for employee matching for each project whenever you upload a new employee, integrated the brute force algorithm with the existing frontend, did a few user interviews, scraped (legally) additional resumes to test our product on
What I aim to do for next sprint: help teammates with whatever they need, work on encryption, finalize algorithm for employee matching

## Sprint 3
1. Krrish Chawla
What I did: Incorporated data masking with the app, strategized on resume chunking, did error handling in the app, front end (LLM reasoning on dashboard), code clean.
What I aim to do for next sprint: Further test data masking, work on LLM prompt optimization with DSPy to get best results, more error handling - making the app industry scalable.

2. Arvind Saligrama
What I did: I implemented a zero-centering algorithm for all the embeddings in the database. In my zeroCentering branch, I integrated this algorithm with the app. I also successfully got chunking to work. I wrote an algorithm that extracts each experience from a resume and embeds those experiences.
What I aim to do for next sprint: Finetune our embedding model on some dataset related to resumes and projects. Use chunking and finetuned model in production. 

4. Roy Yuan
What I did: Incorporated handling for reasoning in project description, strategized for best employee selection, did handling for updating all projects if when new employee added is the best employee (for a project)
What I aim to do for next sprint: Help with faster model, help with encrypt, anything LLM related, clean up any final pieces so project is presentable


## Sprint 4
1. Krrish Chawla
What I did: Tested data masking and incorporated it, worked on error handling, testing different models as a final check, finalized front end, cleaned the data pipeline and implemented it in the code.
What I aim to do for next sprint: Demo day! Aim to present it to people with good feedback.

2. Arvind Saligrama
What I did: I scrapped zero-centering. I also switched from Instructor Embeddings to OpenAI's third generation embedding model. I implemented an algorithm to intelligly chunk resumes into experiences and integrated this with our app. For our emebdding filter, I implemented a novel similarity metric that only considers the top two relevant employee experiences. I rewrote our final LLM reasoning layer that decides between shortlisted candidates. We now incorporate all the text within a resume.
What I aim to do for next sprint: Write slides for demo day and give a great pitch.

3. Roy Yuan
What I did: Poster, slides, preparing for demo day. Helped implement final LLM reasoning layer for shortlisted list of candidates. Brainstorming for speeding up the process because my LLM calls were taking a long time, and iterating through all of them was too slow (came up with chunking).
What I aim to do for next sprint: Help teammates get ready for demo day presentation because I am out of town for school athletics.
