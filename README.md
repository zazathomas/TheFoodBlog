# TheFoodBlog
Live version availabe at https://zazathomas.pythonanywhere.com
This is a simple food blog application powered by Django.
This project has minimal blogging features as it stresses more on the security aspect of working with Django
It includes features such as 2FA, rate limiting, logging successful and failed logging attempts, admin-honeypots, captcha, session timeout etc.
Suggestions are highly welcome as i'm new to Django

How-to
clone the repository
create a virtual python environment in the folder of the cloned repository
run pip install -r requirements.txt to get all needed dependencies
This project uses the python-decouple library to hide sensitive passwords such as API keys, AWS access keys and smtp info.
create a .env file in the same folder as the settings.py file and input the variables needed in the settings.py file to get the project working


