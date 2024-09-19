
# Challenge: Medical Image Server

This project involves creating a simple web server in Python to assess the minimum skill level required for the position. The application will consist of both front-end and back-end components.

## Requirements
1. **Login Page**:
   * There will be a simple login page where users can enter their username and password.
   * The credentials will be checked against a database.

2. **Dashboard**:
   * After successfully logging in, users will be directed to a page containing two buttons.  
  
3. **Display Patient Name**:
   * Upon pressing the first button, the web page, using JavaScript, connects back to the server.
   * The server is expected to retrieve and provide the patient name stored in the DICOM volume found in the data directory.
   * Once received, JavaScript will display the patient information.

4. **Display Image**:
   * Pressing the second button will result in the display of the image representing the slice in the middle of the provided DICOM volume.

5. **Logout**:
   * Users have the option to log out to terminate the session.

## Development
1. Fork the Github repository provided to you.
2. Read the instructions provided in this README file carefully and complete the coding challenge accordingly.
3. The only branch provided in the repository is *main*. However, you are free to create and organize additional branches as necessary to complete your work.
4. When you have completed the challenge, please send an email to the person who assigned you the coding challenge to let them know that you have finished and provide them with a link to your repository.

### Running the project
The project should be possible to run and test with docker-compose.  

Run the project:  
`docker-compose up --build`

Test:  
`docker-compose run --rm web-server python -m pytest`

### Technologies
Some of our preferred/recommended technologies include:
* Docker
* Python
* pytest
* pydicom
* Svelte/SvelteKit

## Evaluation of the challenge: What we pay attention to
When evaluating the challenge, we pay attention to several factors to assess the candidate's skills and suitability for the role. Here are some of the key areas that we typically focus on:

### Functionality and completeness
We will check whether the code meets all the requirements specified in the challenge instructions.

Addtionally, we will test the code to see if it handles edge cases and error conditions correctly. This includes things like handling unexpected inputs or error conditions gracefully and ensuring that the code does not crash or produce unexpected results.

### Code quality and organization
We will assess whether the code is easy to read and understand, and whether it follows established best practices for code readability. This includes things like using consistent naming conventions, using clear and concise comments and breaking up code into logical sections.

In addition to the above criteria, we will also pay attention to whether the candidate's code follows established best practices and conventions for programming.

### Git and version control
We will assess whether the candidate is proficient in using Git for version control.

We will assess the frequency and granularity of the candidate's commits, and whether they are making regular and meaningful commits throughout the development process.

We will assess the quality of the candidate's commit messages, including whether they are descriptive and explain the changes made in each commit.

### Documentation
We will assess the quality of the candidate's documentation, including whether it is clear, concise and comprehensive, and whether it provides useful information for other developers who may be working on the code in the future.

We will assess whether the candidate's documentation covers all relevant aspects of the code.

### Testing
We will assess the candidate's approach to testing and quality assurance, including whether they are writing automated tests to ensure code quality and taking steps to prevent and mitigate errors and bugs.
