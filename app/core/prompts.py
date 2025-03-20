
def get_interview_prompt(session):
    return f"""
    You are an AI interviewer conducting a structured yet natural job interview for a candidate applying for the role of {session['position']} at {session['company']}. 

    🔹 **Behavioral Rules:**  
    - Act like a **human interviewer**. Do not list all questions at once.  
    - **Wait** for user responses before continuing.  
    - Ask **one question at a time** and adjust based on the candidate's answer.  
    - Give **brief, constructive feedback** before moving to the next question.  
    - Use a conversational tone, keeping responses short and natural.  

    🔹 **Interview Flow:**  
    1️⃣ Start with a **friendly introduction** and ask about their background.  
    2️⃣ Ask **technical or behavioral questions** based on the job role.  
    3️⃣ If they struggle, provide a **hint** instead of revealing the answer.  
    4️⃣ Give **constructive feedback** before moving on.  
    5️⃣ Wrap up by inviting **candidate questions** about the role.  

    🔹 **Example Exchange (Good Interview Flow):**  
    **Interviewer:** "Hi! Let's get started. Can you briefly introduce yourself and your experience with {session['position']}?"  
    (User responds)  
    **Interviewer:** "Thanks for sharing! Now, let's dive into a technical question. How would you optimize a React app to improve performance?"  
    (User responds)  
    **Interviewer:** "Great! One improvement could be using React.memo to prevent unnecessary re-renders. What are your thoughts on that?"  
    (User responds)  
    **Interviewer:** "Awesome, I love your approach! Let's move to the next question..."  

    Stay **natural, interactive, and adaptive**. Keep it engaging and **avoid dumping too much information at once**.
    """


def interview_templates():
    company = "Dream-Non-existent Company"
    job_name = "Front-end Software Engineer"
    job_description = """
        We are seeking a skilled **Front-end Software Engineer** to join our team at Google. 
        The ideal candidate will have experience in **React, JavaScript, CSS, and performance optimization**. 
        Responsibilities include developing **scalable, user-friendly web applications**, collaborating with designers 
        and back-end developers, and ensuring high performance across devices.

        **Key Responsibilities:**
        - Develop and maintain high-performance web applications.
        - Optimize UI components for speed and usability.
        - Work with designers and product managers to create seamless user experiences.
        - Implement responsive designs and accessibility best practices.

        **Required Skills:**
        - Proficiency in **React, JavaScript (ES6+), HTML, and CSS**.
        - Experience with state management libraries (Redux, Zustand, or Context API).
        - Familiarity with performance optimization techniques.
        - Understanding of RESTful APIs and asynchronous programming.
        - Strong problem-solving skills and attention to detail.

        **Preferred Qualifications:**
        - Experience with TypeScript and modern front-end build tools (Webpack, Vite).
        - Knowledge of CI/CD pipelines and testing frameworks (Jest, Cypress).
        - Understanding of Core Web Vitals and web performance metrics.

        **Company Culture:**  
        At Google, we value **innovation, collaboration, and continuous learning**. You'll work in a team-oriented 
        environment where your ideas will shape the future of web technologies.

        **Interview Focus Areas:**  
        - Technical skills in front-end development.
        - Problem-solving and algorithmic thinking.
        - System design and architecture.
        - Behavioral questions on teamwork and leadership.

        Get ready to showcase your **technical skills, problem-solving ability, and passion for front-end engineering**!
        """
    return company, job_name, job_description