# Machine learning based Attendance System

## Team Members
- [@Mahmoud-Elsanour](https://github.com/Mahmoud-Elsanour)
- [@codsalah](https://github.com/codsalah)
- [@ziad036](https://github.com/ziad036)
- [@maryashraflotfy](https://github.com/maryashraflotfy)
- [@ketenjo](https://github.com/ketenjo)

## Introduction
Welcome to our Attendance System project! This system utilizes a Siamese Neural Network to recognize and record the attendance of students. We've implemented a user-friendly GUI using Tkinter for student registration and attendance viewing. The system employs with Haarcascade to locate faces, and Opencv for attendance details, including names and entry times, are stored in Excel sheets, with a new file generated daily based on the date.

## Siamese Neural Network
The Siamese Neural Network is a unique architecture designed for measuring similarity between two comparable items. In our case, it is employed to determine the similarity between the facial features of students during registration and their appearances during attendance tracking. This enables accurate recognition and efficient attendance marking.

## TensorFlow and Keras
We utilized TensorFlow and Keras for the implementation of the Siamese Neural Network. TensorFlow provides a robust platform for creating and training neural networks, while Keras, being integrated into TensorFlow, simplifies the construction of complex neural network architectures like the Siamese Network.

## Tkinter GUI
The Tkinter GUI provides an intuitive interface for registering new students and viewing daily attendance. The GUI allows users to input student information seamlessly and enhances the overall user experience.

### Process
1. **Student Registration:**
   - User inputs student details via the Tkinter GUI.
   - OpenCV with Haarcascade locates and captures the facial features for each student.
   - The Siamese Neural Network processes and stores the facial features for future comparison.

2. **Attendance Tracking:**
   - During attendance tracking, the system captures live faces using OpenCV and Haarcascade.
   - The Siamese Neural Network compares the captured faces with the registered faces to determine the identity.
   - Attendance details, including the student's name and entry time, are recorded in an Excel sheet for the current date.

3. **Excel Sheet Management:**
   - A new Excel file is created each day, named based on the date.
   - Attendance details for each day are recorded in the respective Excel file.

## Dependencies

- Python
- jupyter notebook
- TensorFlow
- Keras
- OpenCV
- Tkinter


Feel free to explore the codebase, tweak parameters, and enhance the system further!

## Acknowledgments
Special thanks to our dedicated team members who contributed to the success of this project:

- Ziad Sameh
- Mahmoud Ibrahim
- Salah Mohamed
- Mary Ashraf
- Shahd Hany

We appreciate the collaborative effort in bringing this Project to fruition!

