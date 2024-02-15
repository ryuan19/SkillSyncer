import random
from util import extract_text_from_pdf
from llm import GPT4QAModel
import string

first_names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Charles", "Sarah", "Thomas", "Karen", "Daniel", "Nancy", "Matthew", "Lisa",
    "Anthony", "Betty", "Mark", "Margaret", "Steven", "Sandra", "Andrew", "Ashley",
    "Kenneth", "Dorothy", "Joshua", "Emily", "George", "Donna", "Kevin", "Michelle",
    "Brian", "Carol", "Edward", "Amanda", "Ronald", "Melissa", "Timothy", "Deborah"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter"
]

def generate_random_name():
    # Randomly select a first name and last name
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    # Optionally, introduce variation such as capitalization
    first_name = first_name.capitalize()
    last_name = last_name.capitalize()
    
    # Concatenate the first name and last name
    random_name = f"{first_name} {last_name}"
    
    return random_name

def get_personal_data(text) -> dict:
    resume_identity = text[:200]
    prompt = f"""
    Here is some text which contains personal data. I want you to extract the personal data.
    I want you to output a python dictionary, with the key being the type of data, and the
    value being the data itself. For example, if there is a name, the key-value pair in the
    dictionary should be name : 'given full name'. For name, the key should be name, for email
    the key should be email, for phone number, the key should be number, for website, the key should be website, 
    for linkedin, the key should be linkedin, for other, the key should be other. Here is the data: {resume_identity}
    """
    model = GPT4QAModel()
    response = eval(model.answer_question(prompt))
    return response

# def generate_random_name():
#     return ''.join(random.choices(string.ascii_letters, k=10))

def mask_resume(resume, original_data, new_data):
    return resume.replace(original_data, new_data)

def demask_resume(resume, original_data, new_data):
    return resume.replace(new_data, original_data)

def main():
    pdf = './resume.pdf'
    resume = extract_text_from_pdf(pdf)
    personal_data = get_personal_data(resume)
    print(personal_data)
    
    # Dictionary to store the mapping between real names and fake names
    name_mapping = {}
    
    masked_resume = resume
    for key, value in personal_data.items():
        if key == 'name':
            random_name = generate_random_name()
            name_mapping[value] = random_name  # Store the mapping
            masked_resume = mask_resume(masked_resume, value, random_name)
        else:
            masked_resume = mask_resume(masked_resume, value, str(key))
    
    print(masked_resume)
    
    # Print the name mapping
    print("Name Mapping:")
    for real_name, fake_name in name_mapping.items():
        print(f"{real_name} -> {fake_name}")

if __name__ == '__main__':
    main()
