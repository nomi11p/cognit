# skill.py

def apply_skill(prompt, skill="normal"):

    skills = {

        "normal":
        f"""
        Answer naturally and helpfully.

        User:
        {prompt}
        """,

        "python":
        f"""
        You are an expert Python developer.

        User:
        {prompt}
        """,

        "html":
        f"""
        You are an expert HTML developer.

        User:
        {prompt}
        """,

        "css":
        f"""
        You are an expert CSS developer.

        User:
        {prompt}
        """,

        "javascript":
        f"""
        You are an expert JavaScript developer.

        User:
        {prompt}
        """,

        "email":
        f"""
        Write a professional email.

        User:
        {prompt}
        """
    }

    return skills.get(skill, skills["normal"])