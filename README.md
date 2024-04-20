# Secret: A Secure Solution for Passwords and Files

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
   - [Password Management](#password-management)
     - [Create and Open Password Database](#create-and-open-password-database)
     - [Add, Modify, and Delete Password Records](#add-modify-and-delete-password-records)
     - [Copy Password Fields](#copy-password-fields)
     - [Search and Filter Password Records](#search-and-filter-password-records)
     - [Generate Secure Passwords](#generate-secure-passwords)
     - [Save and Lock Password Database](#save-and-lock-password-database)
     - [Warn of Old Passwords](#warn-of-old-passwords)
     - [Settings](#settings)
   - [File Container](#file-container)
     - [Create and Open Encrypted Container](#create-and-open-encrypted-container)
     - [Add, Modify, and Delete File Records](#add-modify-and-delete-file-records)
     - [Search and Filter File Records](#search-and-filter-file-records)
     - [Save and Lock Container](#save-and-lock-container)
3. [Future Work](#future-work)

## Introduction

Secret is a Python Desktop application developed to address the needs of users who require a secure and convenient way to store and manage their passwords and files on their personal computer. The application provides an encrypted and user-friendly solution for storing and managing sensitive information, without relying on third-party services or cloud storage.
It is compatible with Windows and Linux operating systems and uses tkinter for GUI.

## Features

The software application offers the following key features:

### Password Management

#### Create and Open Password Database
- Users can create a new password database file, which will be encrypted with a master password.
- Users can open an existing password database file by entering the correct master password.

#### Add, Modify, and Delete Password Records
- Users can add new password records to the database, including details such as URL, username, password, notes, and tags.
- Users can modify the details of existing password records.
- Users can delete password records from the database.

#### Copy Password Fields
- Users can copy individual fields (such as username or password) from a password record to their clipboard.

#### Search and Filter Password Records
- Users can search for password records by entering a keyword, and filter the records by username, URL, or tag.

#### Generate Secure Passwords
- Users can generate strong and random passwords using the password generator feature, which also displays the entropy strength measure of the generated password.

#### Save and Lock Password Database
- Users can save the password database file, which will be encrypted with the master password.
- Users can lock the password database file, requiring the master password to be entered again to access it.

#### Warn of Old Passwords
- The system will automatically check the password modification dates and warn the user if any passwords are considered old and need to be changed.

#### Settings
- Users can customize various settings, such as the password warning threshold, number of backups, and password generator options.

### File Container

#### Create and Open Encrypted Container
- Users can create a new encrypted container file, which will be encrypted with a master password.
- Users can open an existing encrypted container file by entering the correct master password.

#### Add, Modify, and Delete File Records
- Users can add new files to the encrypted container, including details such as file name, tag, and notes.
- Users can modify the details of existing file records in the container.
- Users can delete files from the encrypted container.

#### Search and Filter File Records
- Users can search for file records by entering a keyword, and filter the records by file name, tag, or size.

#### Save and Lock Container
- Users can save the encrypted container file, which will be encrypted with the master password.
- Users can lock the encrypted container file, requiring the master password to be entered again to access it.

## Future Work

While the current version of the software application provides a comprehensive set of features, there are a few areas for potential future development:

1. **Expand platform support**: Consider adding support for macOS to further broaden the application's reach.
2. **Implement cloud-based synchronization**: Introduce an optional cloud-based synchronization feature, allowing users to access their passwords and files across multiple devices.
3. **Enhance security features**: Explore additional security measures, such as biometric authentication or two-factor authentication, to further strengthen the protection of the customer's sensitive information.
4. **Improve user experience**: Continuously gather feedback from users and implement enhancements to the graphical user interface, based on user preferences and usability considerations.
