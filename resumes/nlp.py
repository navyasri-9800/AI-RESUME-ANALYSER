import re

SKILLS = [
    'python',
    'java',
    'c',
    'c++',
    'javascript',
    'typescript',
    'html',
    'css',
    'react',
    'django',
    'flask',
    'node.js',
    'express',
    'mysql',
    'postgresql',
    'mongodb',
    'sql',
    'git',
    'github',
    'docker',
    'aws',
    'azure',
    'machine learning',
    'deep learning',
    'data science',
    'rest api',
]


def extract_skills(text):
    if not text:
        return []

    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS:
        pattern = r'(?<![a-zA-Z0-9+#])' + re.escape(skill) + r'(?![a-zA-Z0-9+#])'
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills