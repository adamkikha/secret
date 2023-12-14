<h1 align="center">Secret</h1>

## Introduction
This project aims to develop a user-friendly desktop application for secure password management and encrypted file storage. Employing encryption and hashing techniques, the application ensures data protection from unauthorized access.

## Purpose
The purpose of this project is to develop a software application called Secret that allows users to securely store and manage their passwords and files. Secret will provide a graphical user interface (GUI) in Python that enables users to create, open, and close password database files and encrypted container files. The application will also warn users about old passwords, users will also be able to generate strong passwords, add, modify, and delete records, search by any field, filter by tags, and backup their data.

## Definitions
- Password database file: A file that contains all the relevant information for each password record, such as ID, URL, username, password, notes, tags, and modification date. Each user can have their own password database file, which will be encrypted with a master password.
- Encryption: Reversible transformation of data into an unreadable form using a secret key.
- Encrypted container file: A file that contains other files that are encrypted with a password. Users can create, open, and close encrypted container files to store any type of file they want to protect.
- Password generator: A feature that allows users to generate random passwords of a specified length and character set. The password generator will also display the entropy strength measure of the generated password, which indicates how difficult it is to guess or crack.
- Auto backup: A feature that automatically saves the last x changes in password database files in separate copies. This will help users to recover their data in case of accidental deletion or corruption.
- Entropy measure: A measure of how unpredictable a password is, based on the number of possible combinations of characters. The higher the entropy, the more secure the password is.

## Goals and Objectives
The main goal of this project is to provide users with a convenient and secure way to store and manage their passwords and files. The objectives are:
- To design and implement a user-friendly GUI in Python that supports the main functionalities of Secret.
- To use encryption algorithms and techniques to ensure the confidentiality and integrity of the password database files and the encrypted container files.
- To implement a password generator that can produce strong and random passwords and display their entropy strength measure.
- To implement a search and filter feature that can help users to find the records or files they need quickly and easily.
- To implement an auto backup feature that can save the last x changes in password database files and prevent data loss.
- To follow standard security practices and principles throughout the development process, such as input validation, error handling, and testing.
- To document the requirements, design, implementation, and testing of the application in a clear and comprehensive report.

## Plan
The plan for this project is to follow the incremental development method, which involves dividing the project into small and manageable increments and delivering them in cycles. Each increment will consist of a subset of the functionalities of Secret, and each cycle will consist of the following phases:
- Requirements analysis: In this phase, the functional and non-functional requirements for each increment will be defined and documented.
- Design: In this phase, the system architecture and application architecture for each increment will be designed.
- Implementation: In this phase, the code for each increment will be written in Python, following the test-driven development (TDD) approach. This means that before writing any code, hard-coded tests will be written to verify the functionality of the code. Only after these tests are in place, the code will be written to pass them. This process will be clearly evident in the commit history on GitHub, which will be used to manage the source code and version control.
- Testing: In this phase, the code for each increment will be tested using the hard-coded tests and other testing techniques, such as development testing and release testing. Any bugs or errors will be fixed and documented.
- Evaluation: In this phase, the code for each increment will be evaluated against the requirements and the design, and any feedback or changes will be incorporated in the next cycle.

The project will be completed when all the increments are delivered and integrated into a final product that meets the goals and objectives of the project, and all the documentation is completed.

## Deliverables
- User and System Requirements (functional and non-functional)
- GitHub Repository (Source Code)
- Final Report including Architectural Design, and UML Models (with description)
- Presentation Video
