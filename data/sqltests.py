SQL_TESTS = [
  {
    "question": "Show all student details for those who have a GPA of 3.7 or higher. Return all columns.",
    "sql": "SELECT * FROM students WHERE gpa >= 3.7;"
  },
  {
    "question": "List the names of all tenured professors. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE is_tenured = TRUE;"
  },
  {
    "question": "Which departments have a budget exceeding 1,500,000? Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments WHERE budget > 1500000;"
  },
  {
    "question": "List all courses that carry exactly 4 credits. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE credits = 4;"
  },
  {
    "question": "Retrieve the details of all offerings taught during the Fall semester of 2024. Return all columns.",
    "sql": "SELECT * FROM offerings WHERE semester = 'Fall' AND year = 2024;"
  },
  {
    "question": "Find all students who are in their first year of study. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE year_of_study = 1;"
  },
  {
    "question": "List all professors hired after January 1st, 2021, ordered by their hire date. Return exactly these columns in order: first_name, last_name, hire_date.",
    "sql": "SELECT first_name, last_name, hire_date FROM professors WHERE hire_date > '2021-01-01' ORDER BY hire_date ASC;"
  },
  {
    "question": "Find all departments that are located in the building 'Smith Hall'. Return exactly these columns in order: dept_name.",
    "sql": "SELECT dept_name FROM departments WHERE building = 'Smith Hall';"
  },
  {
    "question": "Get a list of course codes and titles with a maximum enrollment capacity of under 30 students. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE max_enrollment < 30;"
  },
  {
    "question": "Find the details of students who have a GPA between 3.0 and 3.5, inclusive. Return exactly these columns in order: student_id, first_name, last_name, gpa.",
    "sql": "SELECT student_id, first_name, last_name, gpa FROM students WHERE gpa BETWEEN 3.0 AND 3.5;"
  },
  {
    "question": "Show the list of professors whose last name starts with the letter 'M'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE last_name LIKE 'M%';"
  },
  {
    "question": "List all students who are expected to graduate on or before June 15th, 2027. Return exactly these columns in order: first_name, last_name, graduation_date.",
    "sql": "SELECT first_name, last_name, graduation_date FROM students WHERE graduation_date <= '2027-06-15';"
  },
  {
    "question": "Find the salaries and names of professors earning more than 120,000, ordered from highest to lowest salary. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE salary > 120000 ORDER BY salary DESC;"
  },
  {
    "question": "List all distinct semesters available in the offerings table. Return exactly these columns in order: semester.",
    "sql": "SELECT DISTINCT semester FROM offerings;"
  },
  {
    "question": "Retrieve the first 10 students enrolled in the system, sorted by their last names alphabetically. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students ORDER BY last_name ASC LIMIT 10;"
  },
  {
    "question": "Find all enrollments that received a grade of 'A' or 'A-'. Return exactly these columns in order: enrollment_id, offering_id, student_id, grade.",
    "sql": "SELECT enrollment_id, offering_id, student_id, grade FROM enrollments WHERE grade IN ('A', 'A-');"
  },
  {
    "question": "Which courses have course codes containing 'CS' in them? Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE course_code LIKE '%CS%';"
  },
  {
    "question": "List the details of departments that do not have a dean assigned (dean_id is null). Return all columns.",
    "sql": "SELECT * FROM departments WHERE dean_id IS NULL;"
  },
  {
    "question": "Find all professors who are not tenured. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE is_tenured = FALSE;"
  },
  {
    "question": "List all students whose graduation date is not specified. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE graduation_date IS NULL;"
  },
  {
    "question": "Find all enrollments recorded between September 1st, 2024 and September 15th, 2024. Return exactly these columns in order: enrollment_id, student_id, grade.",
    "sql": "SELECT enrollment_id, student_id, grade FROM enrollments WHERE enrollment_date BETWEEN '2024-09-01' AND '2024-09-15';"
  },
  {
    "question": "Show details of the 5 highest-paid professors. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors ORDER BY salary DESC LIMIT 5;"
  },
  {
    "question": "Identify courses with credits ranging between 2 and 4 credits. Return exactly these columns in order: title, credits.",
    "sql": "SELECT title, credits FROM courses WHERE credits BETWEEN 2 AND 4;"
  },
  {
    "question": "List the course code and max enrollment for courses with a capacity of 150 or more students. Return exactly these columns in order: course_code, max_enrollment.",
    "sql": "SELECT course_code, max_enrollment FROM courses WHERE max_enrollment >= 150;"
  },
  {
    "question": "Find all students currently in their 5th or 6th year of study. Return exactly these columns in order: first_name, last_name, year_of_study.",
    "sql": "SELECT first_name, last_name, year_of_study FROM students WHERE year_of_study IN (5, 6);"
  },
  {
    "question": "Get all distinct buildings where university departments are located. Return exactly these columns in order: building.",
    "sql": "SELECT DISTINCT building FROM departments WHERE building IS NOT NULL;"
  },
  {
    "question": "Show all offerings of courses during the year 2025. Return all columns.",
    "sql": "SELECT * FROM offerings WHERE year = 2025;"
  },
  {
    "question": "Find all professors whose salaries are below 60,000. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE salary < 60000;"
  },
  {
    "question": "Search for students whose first name is 'David'. Return exactly these columns in order: student_id, last_name, gpa.",
    "sql": "SELECT student_id, last_name, gpa FROM students WHERE first_name = 'David';"
  },
  {
    "question": "Which departments have a budget that is between 400,000 and 900,000? Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments WHERE budget BETWEEN 400000 AND 900000;"
  },
  {
    "question": "Retrieve offerings taught in the Summer semester. Return exactly these columns in order: offering_id, course_id, prof_id.",
    "sql": "SELECT offering_id, course_id, prof_id FROM offerings WHERE semester = 'Summer';"
  },
  {
    "question": "Find courses whose titles start with the word 'Introduction'. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE title LIKE 'Introduction%';"
  },
  {
    "question": "Find the last name, GPA, and year of study of students who have a GPA strictly below 2.0. Return exactly these columns in order: last_name, gpa, year_of_study.",
    "sql": "SELECT last_name, gpa, year_of_study FROM students WHERE gpa < 2.0;"
  },
  {
    "question": "List the distinct grades given in all course enrollments. Return exactly these columns in order: grade.",
    "sql": "SELECT DISTINCT grade FROM enrollments WHERE grade IS NOT NULL;"
  },
  {
    "question": "List the names of professors hired in the year 2019. Return exactly these columns in order: first_name, last_name, hire_date.",
    "sql": "SELECT first_name, last_name, hire_date FROM professors WHERE hire_date BETWEEN '2019-01-01' AND '2019-12-31';"
  },
  {
    "question": "List the names and codes of the three courses with the absolute lowest enrollment limits. Return exactly these columns in order: course_code, title, max_enrollment.",
    "sql": "SELECT course_code, title, max_enrollment FROM courses ORDER BY max_enrollment ASC LIMIT 3;"
  },
  {
    "question": "Find students who have 'Johnson' as their last name. Return exactly these columns in order: student_id, first_name, gpa.",
    "sql": "SELECT student_id, first_name, gpa FROM students WHERE last_name = 'Johnson';"
  },
  {
    "question": "Show the list of department names sorted in descending alphabetical order. Return exactly these columns in order: dept_name.",
    "sql": "SELECT dept_name FROM departments ORDER BY dept_name DESC;"
  },
  {
    "question": "Which course offerings were conducted in the year 2023 but specifically not in the Summer? Return exactly these columns in order: offering_id, course_id, semester.",
    "sql": "SELECT offering_id, course_id, semester FROM offerings WHERE year = 2023 AND semester != 'Summer';"
  },
  {
    "question": "List professors who do not belong to any department (dept_id is null). Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE dept_id IS NULL;"
  },
  {
    "question": "Find the 5 most recently hired professors. Return exactly these columns in order: first_name, last_name, hire_date.",
    "sql": "SELECT first_name, last_name, hire_date FROM professors ORDER BY hire_date DESC LIMIT 5;"
  },
  {
    "question": "Show the details of all departments located in building 'Science Center'. Return all columns.",
    "sql": "SELECT * FROM departments WHERE building = 'Science Center';"
  },
  {
    "question": "List course codes that end with the number '101'. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE course_code LIKE '%101';"
  },
  {
    "question": "Identify students who are in their 2nd, 3rd, or 4th year of study. Return exactly these columns in order: first_name, last_name, year_of_study.",
    "sql": "SELECT first_name, last_name, year_of_study FROM students WHERE year_of_study BETWEEN 2 AND 4;"
  },
  {
    "question": "Find the enrollments where students received a grade of 'F' or 'W'. Return all columns.",
    "sql": "SELECT * FROM enrollments WHERE grade IN ('F', 'W');"
  },
  {
    "question": "Find students whose last name contains the letters 'son'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE last_name LIKE '%son%';"
  },
  {
    "question": "List all tenured professors with a salary greater than 90,000, sorted by salary. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE is_tenured = TRUE AND salary > 90000 ORDER BY salary DESC;"
  },
  {
    "question": "Show offerings of course ID 5. Return exactly these columns in order: offering_id, semester, year.",
    "sql": "SELECT offering_id, semester, year FROM offerings WHERE course_id = 5;"
  },
  {
    "question": "List students who graduated or will graduate in the year 2026. Return exactly these columns in order: first_name, last_name, graduation_date.",
    "sql": "SELECT first_name, last_name, graduation_date FROM students WHERE graduation_date BETWEEN '2026-01-01' AND '2026-12-31';"
  },
  {
    "question": "Show details of the department with dean ID equal to 12. Return all columns.",
    "sql": "SELECT * FROM departments WHERE dean_id = 12;"
  },
  {
    "question": "Get courses that are 1 credit hour. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE credits = 1;"
  },
  {
    "question": "List the first names and last names of students with GPA exactly equal to 4.0. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE gpa = 4.0;"
  },
  {
    "question": "Find all enrollments recorded before January 1, 2023. Return all columns.",
    "sql": "SELECT * FROM enrollments WHERE enrollment_date < '2023-01-01';"
  },
  {
    "question": "Find professors who have a salary between 70,000 and 100,000. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE salary BETWEEN 70000 AND 100000;"
  },
  {
    "question": "List the first and last name of students whose year of study is greater than 3, ordered by year of study descending. Return exactly these columns in order: first_name, last_name, year_of_study.",
    "sql": "SELECT first_name, last_name, year_of_study FROM students WHERE year_of_study > 3 ORDER BY year_of_study DESC;"
  },
  {
    "question": "Show details of courses that have a maximum enrollment of exactly 50. Return all columns.",
    "sql": "SELECT * FROM courses WHERE max_enrollment = 50;"
  },
  {
    "question": "Find all offerings from the Spring semester of 2022. Return exactly these columns in order: offering_id, course_id, prof_id.",
    "sql": "SELECT offering_id, course_id, prof_id FROM offerings WHERE semester = 'Spring' AND year = 2022;"
  },
  {
    "question": "Which departments have a budget of less than 300,000? Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments WHERE budget < 300000;"
  },
  {
    "question": "Find all students whose first name starts with 'J' and ends with 'n'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE first_name LIKE 'J%n';"
  },
  {
    "question": "List all departments, ordered by their budget ascending. Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments ORDER BY budget ASC;"
  },
  {
    "question": "Retrieve courses belonging to department ID 3. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE dept_id = 3;"
  },
  {
    "question": "Find professors who were hired in June of any year. Return exactly these columns in order: first_name, last_name, hire_date.",
    "sql": "SELECT first_name, last_name, hire_date FROM professors WHERE hire_date LIKE '%-06-%';"
  },
  {
    "question": "List all students whose GPA is less than 2.5 and who are in their first year. Return exactly these columns in order: first_name, last_name, gpa.",
    "sql": "SELECT first_name, last_name, gpa FROM students WHERE gpa < 2.5 AND year_of_study = 1;"
  },
  {
    "question": "Find the course offerings of course ID 10 in the Fall semester. Return exactly these columns in order: offering_id, year.",
    "sql": "SELECT offering_id, year FROM offerings WHERE course_id = 10 AND semester = 'Fall';"
  },
  {
    "question": "Which enrollments have a grade of 'C' or below (C+, C, D, F)? Return exactly these columns in order: enrollment_id, student_id, grade.",
    "sql": "SELECT enrollment_id, student_id, grade FROM enrollments WHERE grade IN ('C+', 'C', 'D', 'F');"
  },
  {
    "question": "Get the names of all tenured professors in department 2. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE is_tenured = TRUE AND dept_id = 2;"
  },
  {
    "question": "Show course title and max enrollment for courses with more than 3 credits. Return exactly these columns in order: title, max_enrollment.",
    "sql": "SELECT title, max_enrollment FROM courses WHERE credits > 3;"
  },
  {
    "question": "List all students with last name 'Smith' or first name 'John'. Return exactly these columns in order: student_id, first_name, last_name.",
    "sql": "SELECT student_id, first_name, last_name FROM students WHERE last_name = 'Smith' OR first_name = 'John';"
  },
  {
    "question": "What is the department ID of the department with name 'Chemistry'? Return exactly these columns in order: dept_id.",
    "sql": "SELECT dept_id FROM departments WHERE dept_name = 'Chemistry';"
  },
  {
    "question": "List the details of the top 3 students by GPA in their 4th year. Return all columns.",
    "sql": "SELECT * FROM students WHERE year_of_study = 4 ORDER BY gpa DESC LIMIT 3;"
  },
  {
    "question": "Which professors have a null hire date? Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE hire_date IS NULL;"
  },
  {
    "question": "Find all courses that do not belong to department ID 1. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE dept_id != 1 OR dept_id IS NULL;"
  },
  {
    "question": "List all offerings that are not scheduled for the year 2024. Return all columns.",
    "sql": "SELECT * FROM offerings WHERE year != 2024;"
  },
  {
    "question": "Retrieve student first name and last name where student ID is between 100 and 150. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE student_id BETWEEN 100 AND 150;"
  },
  {
    "question": "Find the building name for the department named 'Computer Science'.",
    "sql": "SELECT building FROM departments WHERE dept_name = 'Computer Science';"
  },
  {
    "question": "Select courses with credit values of 2, 3, or 4. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE credits IN (2, 3, 4);"
  },
  {
    "question": "List all students whose graduation date is set after the year 2028. Return exactly these columns in order: first_name, last_name, graduation_date.",
    "sql": "SELECT first_name, last_name, graduation_date FROM students WHERE graduation_date > '2028-12-31';"
  },
  {
    "question": "Find all enrollments with enrollment date equal to '2024-08-25'. Return all columns.",
    "sql": "SELECT * FROM enrollments WHERE enrollment_date = '2024-08-25';"
  },
  {
    "question": "Retrieve details of department number 5. Return all columns.",
    "sql": "SELECT * FROM departments WHERE dept_id = 5;"
  },
  {
    "question": "Find professors who have a salary of exactly 80,000. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE salary = 80000;"
  },
  {
    "question": "Retrieve the first name, last name, and department name of all students. Return exactly these columns in order: first_name, last_name, dept_name.",
    "sql": "SELECT s.first_name, s.last_name, d.dept_name FROM students s JOIN departments d ON s.major_dept_id = d.dept_id;"
  },
  {
    "question": "Find the names of all professors along with the name of their department. Return exactly these columns in order: first_name, last_name, dept_name.",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name FROM professors p JOIN departments d ON p.dept_id = d.dept_id;"
  },
  {
    "question": "Show the first name, last name, and grade of students enrolled in any course offering. Return exactly these columns in order: first_name, last_name, grade.",
    "sql": "SELECT s.first_name, s.last_name, e.grade FROM students s JOIN enrollments e ON s.student_id = e.student_id;"
  },
  {
    "question": "List all course titles and the names of the departments offering them. Return exactly these columns in order: title, dept_name.",
    "sql": "SELECT c.title, d.dept_name FROM courses c JOIN departments d ON c.dept_id = d.dept_id;"
  },
  {
    "question": "Show all offerings of courses with the course title and the corresponding semester and year.",
    "sql": "SELECT c.title, o.semester, o.year FROM offerings o JOIN courses c ON o.course_id = c.course_id;"
  },
  {
    "question": "Retrieve the first and last names of deans and the department they manage. Return exactly these columns in order: first_name, last_name, dept_name.",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name FROM departments d JOIN professors p ON d.dean_id = p.prof_id;"
  },
  {
    "question": "Get the list of courses and the name of the professor teaching each of their offerings. Return exactly these columns in order: title, first_name, last_name.",
    "sql": "SELECT c.title, p.first_name, p.last_name FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN professors p ON o.prof_id = p.prof_id;"
  },
  {
    "question": "Find the students enrolled in course offerings for 'Fall 2024' along with their grades. Return exactly these columns in order: first_name, last_name, grade.",
    "sql": "SELECT s.first_name, s.last_name, e.grade FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id WHERE o.semester = 'Fall' AND o.year = 2024;"
  },
  {
    "question": "Display all course codes and names, along with the details of their department's building. Return exactly these columns in order: course_code, title, building.",
    "sql": "SELECT c.course_code, c.title, d.building FROM courses c JOIN departments d ON c.dept_id = d.dept_id;"
  },
  {
    "question": "Get the names of all students majoring in departments located in the 'Science Hall'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT s.first_name, s.last_name FROM students s JOIN departments d ON s.major_dept_id = d.dept_id WHERE d.building = 'Science Hall';"
  },
  {
    "question": "Show the list of students, the course titles they are enrolled in, and the semester. Return exactly these columns in order: first_name, last_name, title, semester.",
    "sql": "SELECT s.first_name, s.last_name, c.title, o.semester FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id;"
  },
  {
    "question": "List all departments and include their dean's first and last name, if they have a dean. Return exactly these columns in order: dept_name, first_name, last_name.",
    "sql": "SELECT d.dept_name, p.first_name, p.last_name FROM departments d LEFT JOIN professors p ON d.dean_id = p.prof_id;"
  },
  {
    "question": "List all professors, and for those who belong to a department, show the department name and budget. Return exactly these columns in order: first_name, last_name, dept_name, budget.",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name, d.budget FROM professors p LEFT JOIN departments d ON p.dept_id = d.dept_id;"
  },
  {
    "question": "Find all courses offered in 2025, including those courses that were not offered at all (show nulls for offerings). Return exactly these columns in order: title, semester, year.",
    "sql": "SELECT c.title, o.semester, o.year FROM courses c LEFT JOIN offerings o ON c.course_id = o.course_id AND o.year = 2025;"
  },
  {
    "question": "List students and their enrollment grades for the course 'CS101' (even if they have no enrollments). Return exactly these columns in order: first_name, last_name, grade.",
    "sql": "SELECT s.first_name, s.last_name, e.grade FROM students s LEFT JOIN enrollments e ON s.student_id = e.student_id LEFT JOIN offerings o ON e.offering_id = o.offering_id LEFT JOIN courses c ON o.course_id = c.course_id AND c.course_code = 'CS101';"
  },
  {
    "question": "Which students are enrolled in a course taught by Professor 'Robert Smith'? Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN professors p ON o.prof_id = p.prof_id WHERE p.first_name = 'Robert' AND p.last_name = 'Smith';"
  },
  {
    "question": "List all department budgets alongside the names of students majoring in them. Return exactly these columns in order: dept_name, budget, first_name, last_name.",
    "sql": "SELECT d.dept_name, d.budget, s.first_name, s.last_name FROM departments d JOIN students s ON d.dept_id = s.major_dept_id;"
  },
  {
    "question": "Show the list of courses with their maximum enrollment and the department dean's name. Return exactly these columns in order: title, max_enrollment, first_name, last_name.",
    "sql": "SELECT c.title, c.max_enrollment, p.first_name, p.last_name FROM courses c JOIN departments d ON c.dept_id = d.dept_id JOIN professors p ON d.dean_id = p.prof_id;"
  },
  {
    "question": "List all tenured professors who are deans of departments. Return exactly these columns in order: first_name, last_name, dept_name.",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name FROM professors p JOIN departments d ON p.prof_id = d.dean_id WHERE p.is_tenured = TRUE;"
  },
  {
    "question": "Find students who received an 'A' grade in any course taught in 'Spring 2023'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT s.first_name, s.last_name FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id WHERE e.grade = 'A' AND o.semester = 'Spring' AND o.year = 2023;"
  },
  {
    "question": "Find the course title, code, and offering details for all offerings taught by tenured professors. Return exactly these columns in order: title, course_code, semester, year.",
    "sql": "SELECT c.title, c.course_code, o.semester, o.year FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN professors p ON o.prof_id = p.prof_id WHERE p.is_tenured = TRUE;"
  },
  {
    "question": "Show the names of students who are enrolled in offerings of 'Physics' courses. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id JOIN departments d ON c.dept_id = d.dept_id WHERE d.dept_name = 'Physics';"
  },
  {
    "question": "List the first name, last name, and major department of students who have a GPA higher than 3.8 and are majoring in a department located in building 'North Hall'. Return exactly these columns in order: first_name, last_name, dept_name.",
    "sql": "SELECT s.first_name, s.last_name, d.dept_name FROM students s JOIN departments d ON s.major_dept_id = d.dept_id WHERE s.gpa > 3.8 AND d.building = 'North Hall';"
  },
  {
    "question": "Find the names of deans whose departments have a budget greater than 1,000,000. Return exactly these columns in order: first_name, last_name, dept_name, budget.",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name, d.budget FROM departments d JOIN professors p ON d.dean_id = p.prof_id WHERE d.budget > 1000000;"
  },
  {
    "question": "List all departments, and if they offer courses, list the titles of those courses. Return exactly these columns in order: dept_name, title.",
    "sql": "SELECT d.dept_name, c.title FROM departments d LEFT JOIN courses c ON d.dept_id = c.dept_id;"
  },
  {
    "question": "For all offerings, display the course code, semester, year, and the instructor's last name. Return exactly these columns in order: course_code, semester, year, last_name.",
    "sql": "SELECT c.course_code, o.semester, o.year, p.last_name FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN professors p ON o.prof_id = p.prof_id;"
  },
  {
    "question": "Retrieve all students whose major department is the same department that offers 'CS201'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name FROM students s JOIN departments d ON s.major_dept_id = d.dept_id JOIN courses c ON d.dept_id = c.dept_id WHERE c.course_code = 'CS201';"
  },
  {
    "question": "List students who have enrollment records along with the names of the professors teaching their enrolled courses. Return exactly these columns in order: student_first, student_last, prof_first, prof_last.",
    "sql": "SELECT DISTINCT s.first_name AS student_first, s.last_name AS student_last, p.first_name AS prof_first, p.last_name AS prof_last FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN professors p ON o.prof_id = p.prof_id;"
  },
  {
    "question": "Find all courses offered in 'Fall 2024' that are managed by a department with a budget less than 500,000. Return exactly these columns in order: title, course_code.",
    "sql": "SELECT DISTINCT c.title, c.course_code FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN departments d ON c.dept_id = d.dept_id WHERE o.semester = 'Fall' AND o.year = 2024 AND d.budget < 500000;"
  },
  {
    "question": "Retrieve a list of student first and last names along with their major department name, including students who do not have a declared major department. Return exactly these columns in order: first_name, last_name, dept_name.",
    "sql": "SELECT s.first_name, s.last_name, d.dept_name FROM students s LEFT JOIN departments d ON s.major_dept_id = d.dept_id;"
  },
  {
    "question": "Show all enrollment dates and student names for course offerings taught by professors with 'Mathematics' in their department name. Return exactly these columns in order: enrollment_date, first_name, last_name.",
    "sql": "SELECT e.enrollment_date, s.first_name, s.last_name FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN professors p ON o.prof_id = p.prof_id JOIN departments d ON p.dept_id = d.dept_id WHERE d.dept_name LIKE '%Mathematics%';"
  },
  {
    "question": "Retrieve all students and any offerings they are enrolled in for the year 2024. Return exactly these columns in order: first_name, last_name, offering_id, semester.",
    "sql": "SELECT s.first_name, s.last_name, e.offering_id, o.semester FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN offerings o ON e.offering_id = o.offering_id WHERE o.year = 2024;"
  },
  {
    "question": "Get the names of all professors whose department dean is tenured. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT p.first_name, p.last_name FROM professors p JOIN departments d ON p.dept_id = d.dept_id JOIN professors dean ON d.dean_id = dean.prof_id WHERE dean.is_tenured = TRUE;"
  },
  {
    "question": "Find all offerings of courses with details about whether the professor is tenured. Return exactly these columns in order: title, last_name, is_tenured, semester, year.",
    "sql": "SELECT c.title, p.last_name, p.is_tenured, o.semester, o.year FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN professors p ON o.prof_id = p.prof_id;"
  },
  {
    "question": "List the course titles and offering information of all courses with credit hours equal to 3. Return exactly these columns in order: title, semester, year.",
    "sql": "SELECT c.title, o.semester, o.year FROM offerings o JOIN courses c ON o.course_id = c.course_id WHERE c.credits = 3;"
  },
  {
    "question": "Show students' full names and the buildings of their major departments for students who have a GPA of 3.9 or higher. Return exactly these columns in order: first_name, last_name, building.",
    "sql": "SELECT s.first_name, s.last_name, d.building FROM students s JOIN departments d ON s.major_dept_id = d.dept_id WHERE s.gpa >= 3.9;"
  },
  {
    "question": "List all courses, and if they have enrollment records, show the enrollment dates and grades. Return exactly these columns in order: title, enrollment_date, grade.",
    "sql": "SELECT c.title, e.enrollment_date, e.grade FROM courses c LEFT JOIN offerings o ON c.course_id = o.course_id LEFT JOIN enrollments e ON o.offering_id = e.offering_id;"
  },
  {
    "question": "Retrieve the first name, last name, and department name of professors who earn more than 110,000 and are tenured. Return exactly these columns in order: first_name, last_name, dept_name.",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name FROM professors p JOIN departments d ON p.dept_id = d.dept_id WHERE p.salary > 110000 AND p.is_tenured = TRUE;"
  },
  {
    "question": "Find the student names and course titles where students received a 'W' grade. Return exactly these columns in order: first_name, last_name, title.",
    "sql": "SELECT s.first_name, s.last_name, c.title FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id WHERE e.grade = 'W';"
  },
  {
    "question": "Get the names of all deans whose hired date is before 2015. Return exactly these columns in order: first_name, last_name, dept_name.",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name FROM departments d JOIN professors p ON d.dean_id = p.prof_id WHERE p.hire_date < '2015-01-01';"
  },
  {
    "question": "Retrieve students whose last name is 'Miller' along with their major department's dean's name. Return exactly these columns in order: student_first, student_last, dept_name, dean_first, dean_last.",
    "sql": "SELECT s.first_name AS student_first, s.last_name AS student_last, d.dept_name, p.first_name AS dean_first, p.last_name AS dean_last FROM students s JOIN departments d ON s.major_dept_id = d.dept_id JOIN professors p ON d.dean_id = p.prof_id WHERE s.last_name = 'Miller';"
  },
  {
    "question": "List course titles and their max enrollment for all courses offered in the 'Summer' semester. Return exactly these columns in order: title, max_enrollment.",
    "sql": "SELECT DISTINCT c.title, c.max_enrollment FROM offerings o JOIN courses c ON o.course_id = c.course_id WHERE o.semester = 'Summer';"
  },
  {
    "question": "Find the names of students majoring in 'Biology' who are in their 3rd year of study. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT s.first_name, s.last_name FROM students s JOIN departments d ON s.major_dept_id = d.dept_id WHERE d.dept_name = 'Biology' AND s.year_of_study = 3;"
  },
  {
    "question": "List all courses along with their offering semesters and years, ensuring we include courses that haven't been offered yet. Return exactly these columns in order: course_code, title, semester, year.",
    "sql": "SELECT c.course_code, c.title, o.semester, o.year FROM courses c LEFT JOIN offerings o ON c.course_id = o.course_id;"
  },
  {
    "question": "Get details of all enrollments by students whose major department is the same department offering the enrolled course. Return exactly these columns in order: first_name, last_name, title, grade.",
    "sql": "SELECT s.first_name, s.last_name, c.title, e.grade FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id WHERE s.major_dept_id = c.dept_id;"
  },
  {
    "question": "Find the list of departments that have at least one professor earning over 130,000. Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT DISTINCT d.dept_name, d.budget FROM departments d JOIN professors p ON d.dept_id = p.dept_id WHERE p.salary > 130000;"
  },
  {
    "question": "Show all offerings taught by professors who were hired before '2010-01-01'. Return exactly these columns in order: title, semester, year, first_name, last_name.",
    "sql": "SELECT c.title, o.semester, o.year, p.first_name, p.last_name FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN professors p ON o.prof_id = p.prof_id WHERE p.hire_date < '2010-01-01';"
  },
  {
    "question": "List all department names along with the number of students majoring in them (even if the student count is zero). Return exactly these columns in order: dept_name, student_count.",
    "sql": "SELECT d.dept_name, COUNT(s.student_id) AS student_count FROM departments d LEFT JOIN students s ON d.dept_id = s.major_dept_id GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "What is the average salary of professors in each department? Return exactly these columns in order: dept_name, average_salary.",
    "sql": "SELECT d.dept_name, AVG(p.salary) AS average_salary FROM departments d JOIN professors p ON d.dept_id = p.dept_id GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "For each department, list the department name and the maximum budget. Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments GROUP BY dept_id, dept_name;"
  },
  {
    "question": "Find the total number of students enrolled in each course offering. Return exactly these columns in order: offering_id, title, semester, year, enrollment_count.",
    "sql": "SELECT o.offering_id, c.title, o.semester, o.year, COUNT(e.enrollment_id) AS enrollment_count FROM offerings o JOIN courses c ON o.course_id = c.course_id LEFT JOIN enrollments e ON o.offering_id = e.offering_id GROUP BY o.offering_id, c.title, o.semester, o.year;"
  },
  {
    "question": "What is the total department budget allocated across all buildings? Return exactly these columns in order: building, total_budget.",
    "sql": "SELECT building, SUM(budget) AS total_budget FROM departments WHERE building IS NOT NULL GROUP BY building;"
  },
  {
    "question": "Find the minimum, maximum, and average GPA of students for each year of study. Return exactly these columns in order: year_of_study, min_gpa, max_gpa, avg_gpa.",
    "sql": "SELECT year_of_study, MIN(gpa) AS min_gpa, MAX(gpa) AS max_gpa, AVG(gpa) AS avg_gpa FROM students GROUP BY year_of_study;"
  },
  {
    "question": "How many professors are tenured versus non-tenured in the entire university? Return exactly these columns in order: is_tenured, prof_count.",
    "sql": "SELECT is_tenured, COUNT(*) AS prof_count FROM professors GROUP BY is_tenured;"
  },
  {
    "question": "List the departments with more than 5 professors. Return exactly these columns in order: dept_name, professor_count.",
    "sql": "SELECT d.dept_name, COUNT(p.prof_id) AS professor_count FROM departments d JOIN professors p ON d.dept_id = p.dept_id GROUP BY d.dept_id, d.dept_name HAVING COUNT(p.prof_id) > 5;"
  },
  {
    "question": "Calculate the average GPA of students in each major department, showing only those with an average GPA above 3.0. Return exactly these columns in order: dept_name, average_gpa.",
    "sql": "SELECT d.dept_name, AVG(s.gpa) AS average_gpa FROM departments d JOIN students s ON d.dept_id = s.major_dept_id GROUP BY d.dept_id, d.dept_name HAVING AVG(s.gpa) > 3.0;"
  },
  {
    "question": "Find the number of courses offered by each department. Return exactly these columns in order: dept_name, total_courses.",
    "sql": "SELECT d.dept_name, COUNT(c.course_id) AS total_courses FROM departments d LEFT JOIN courses c ON d.dept_id = c.dept_id GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "How many student enrollments did each offering have in the 'Fall' of 2024? Return exactly these columns in order: offering_id, title, enrollment_count.",
    "sql": "SELECT o.offering_id, c.title, COUNT(e.enrollment_id) AS enrollment_count FROM offerings o JOIN courses c ON o.course_id = c.course_id LEFT JOIN enrollments e ON o.offering_id = e.offering_id WHERE o.semester = 'Fall' AND o.year = 2024 GROUP BY o.offering_id, c.title;"
  },
  {
    "question": "List the average, maximum, and minimum salaries of professors in departments that have a budget of over 1,000,000. Return exactly these columns in order: dept_name, avg_sal, max_sal, min_sal.",
    "sql": "SELECT d.dept_name, AVG(p.salary) AS avg_sal, MAX(p.salary) AS max_sal, MIN(p.salary) AS min_sal FROM departments d JOIN professors p ON d.dept_id = p.dept_id WHERE d.budget > 1000000 GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "Find the course offering IDs that have more than 50 students enrolled. Return exactly these columns in order: offering_id, total_students.",
    "sql": "SELECT offering_id, COUNT(student_id) AS total_students FROM enrollments GROUP BY offering_id HAVING COUNT(student_id) > 50;"
  },
  {
    "question": "List the name of each student and the total number of credits they are taking in total. Return exactly these columns in order: first_name, last_name, total_credits.",
    "sql": "SELECT s.first_name, s.last_name, SUM(c.credits) AS total_credits FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id GROUP BY s.student_id, s.first_name, s.last_name;"
  },
  {
    "question": "Find the total salary expenditure for each department, ordered from highest to lowest expenditure. Return exactly these columns in order: dept_name, total_salaries.",
    "sql": "SELECT d.dept_name, SUM(p.salary) AS total_salaries FROM departments d JOIN professors p ON d.dept_id = p.dept_id GROUP BY d.dept_id, d.dept_name ORDER BY total_salaries DESC;"
  },
  {
    "question": "List the grades and the total number of students who received each grade in the system. Return exactly these columns in order: grade, count_grade.",
    "sql": "SELECT grade, COUNT(*) AS count_grade FROM enrollments WHERE grade IS NOT NULL GROUP BY grade;"
  },
  {
    "question": "For each professor, find the total number of offerings they have taught. Return exactly these columns in order: first_name, last_name, offerings_taught.",
    "sql": "SELECT p.first_name, p.last_name, COUNT(o.offering_id) AS offerings_taught FROM professors p LEFT JOIN offerings o ON p.prof_id = o.prof_id GROUP BY p.prof_id, p.first_name, p.last_name;"
  },
  {
    "question": "Which semesters have had more than 100 course offerings overall? Return exactly these columns in order: semester, year, total_offerings.",
    "sql": "SELECT semester, year, COUNT(offering_id) AS total_offerings FROM offerings GROUP BY semester, year HAVING COUNT(offering_id) > 100;"
  },
  {
    "question": "Retrieve the names of professors who teach more than 2 offerings in any single semester and year. Return exactly these columns in order: first_name, last_name, semester, year, offerings_count.",
    "sql": "SELECT p.first_name, p.last_name, o.semester, o.year, COUNT(o.offering_id) AS offerings_count FROM professors p JOIN offerings o ON p.prof_id = o.prof_id GROUP BY p.prof_id, p.first_name, p.last_name, o.semester, o.year HAVING COUNT(o.offering_id) > 2;"
  },
  {
    "question": "List the major departments that have a total student GPA average above 3.5. Return exactly these columns in order: dept_name, avg_gpa.",
    "sql": "SELECT d.dept_name, AVG(s.gpa) AS avg_gpa FROM departments d JOIN students s ON d.dept_id = s.major_dept_id GROUP BY d.dept_id, d.dept_name HAVING AVG(s.gpa) > 3.5;"
  },
  {
    "question": "What is the average enrollment size for courses offered by the department 'Computer Science'? Return exactly these columns in order: title, avg_enrollment.",
    "sql": "SELECT c.title, AVG(e_count.enroll_count) AS avg_enrollment FROM courses c JOIN (SELECT e.offering_id, course_id, COUNT(*) AS enroll_count FROM enrollments e JOIN offerings o ON e.offering_id = o.offering_id GROUP BY e.offering_id, course_id) e_count ON c.course_id = e_count.course_id JOIN departments d ON c.dept_id = d.dept_id WHERE d.dept_name = 'Computer Science' GROUP BY c.course_id, c.title;"
  },
  {
    "question": "Count the number of students who are graduating in each year, showing the year and count. Return exactly these columns in order: grad_year, student_count.",
    "sql": "SELECT strftime('%Y', graduation_date) AS grad_year, COUNT(*) AS student_count FROM students WHERE graduation_date IS NOT NULL GROUP BY grad_year;"
  },
  {
    "question": "Which departments have total budgets of all their courses' max enrollments combined exceeding 500? Return exactly these columns in order: dept_name, total_capacity.",
    "sql": "SELECT d.dept_name, SUM(c.max_enrollment) AS total_capacity FROM departments d JOIN courses c ON d.dept_id = c.dept_id GROUP BY d.dept_id, d.dept_name HAVING SUM(c.max_enrollment) > 500;"
  },
  {
    "question": "Find the average salary of tenured professors compared to non-tenured professors in each department. Return exactly these columns in order: dept_name, is_tenured, average_salary.",
    "sql": "SELECT d.dept_name, p.is_tenured, AVG(p.salary) AS average_salary FROM departments d JOIN professors p ON d.dept_id = p.dept_id GROUP BY d.dept_id, d.dept_name, p.is_tenured;"
  },
  {
    "question": "List the titles of courses that have been offered more than 5 times in the university's history. Return exactly these columns in order: title, times_offered.",
    "sql": "SELECT c.title, COUNT(o.offering_id) AS times_offered FROM courses c JOIN offerings o ON c.course_id = o.course_id GROUP BY c.course_id, c.title HAVING COUNT(o.offering_id) > 5;"
  },
  {
    "question": "Find the student majors with at least 10 enrolled students with a GPA over 3.0. Return exactly these columns in order: dept_name, student_count.",
    "sql": "SELECT d.dept_name, COUNT(s.student_id) AS student_count FROM departments d JOIN students s ON d.dept_id = s.major_dept_id WHERE s.gpa > 3.0 GROUP BY d.dept_id, d.dept_name HAVING COUNT(s.student_id) >= 10;"
  },
  {
    "question": "Get the number of course offerings taught by each tenured professor. Return exactly these columns in order: first_name, last_name, total_offerings.",
    "sql": "SELECT p.first_name, p.last_name, COUNT(o.offering_id) AS total_offerings FROM professors p JOIN offerings o ON p.prof_id = o.prof_id WHERE p.is_tenured = TRUE GROUP BY p.prof_id, p.first_name, p.last_name;"
  },
  {
    "question": "Calculate the average GPA of students in their 1st, 2nd, 3rd, and 4th years of study who are majoring in department ID 1. Return exactly these columns in order: year_of_study, avg_gpa.",
    "sql": "SELECT year_of_study, AVG(gpa) AS avg_gpa FROM students WHERE major_dept_id = 1 GROUP BY year_of_study;"
  },
  {
    "question": "Find the building name along with the total number of departments housed in each building. Return exactly these columns in order: building, department_count.",
    "sql": "SELECT building, COUNT(dept_id) AS department_count FROM departments WHERE building IS NOT NULL GROUP BY building;"
  },
  {
    "question": "For each student, show the total number of 'A' grades they have received. Return exactly these columns in order: first_name, last_name, a_count.",
    "sql": "SELECT s.first_name, s.last_name, COUNT(e.enrollment_id) AS a_count FROM students s JOIN enrollments e ON s.student_id = e.student_id WHERE e.grade = 'A' GROUP BY s.student_id, s.first_name, s.last_name;"
  },
  {
    "question": "Find the departments that have a dean but have fewer than 3 professors total. Return exactly these columns in order: dept_name, total_profs.",
    "sql": "SELECT d.dept_name, COUNT(p.prof_id) AS total_profs FROM departments d LEFT JOIN professors p ON d.dept_id = p.dept_id WHERE d.dean_id IS NOT NULL GROUP BY d.dept_id, d.dept_name HAVING COUNT(p.prof_id) < 3;"
  },
  {
    "question": "Show the number of course credits offered by each department. Return exactly these columns in order: dept_name, total_credits.",
    "sql": "SELECT d.dept_name, SUM(c.credits) AS total_credits FROM departments d JOIN courses c ON d.dept_id = c.dept_id GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "Find the total number of students enrolled in offerings taught by each professor. Return exactly these columns in order: first_name, last_name, students_taught.",
    "sql": "SELECT p.first_name, p.last_name, COUNT(e.enrollment_id) AS students_taught FROM professors p JOIN offerings o ON p.prof_id = o.prof_id LEFT JOIN enrollments e ON o.offering_id = e.offering_id GROUP BY p.prof_id, p.first_name, p.last_name;"
  },
  {
    "question": "Find the average GPA of students who enrolled in courses during the year 2024. Return exactly these columns in order: average_gpa.",
    "sql": "SELECT AVG(s.gpa) AS average_gpa FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN offerings o ON e.offering_id = o.offering_id WHERE o.year = 2024;"
  },
  {
    "question": "What is the maximum salary earned by a professor in each department, excluding those that do not have tenured professors? Return exactly these columns in order: dept_name, max_salary.",
    "sql": "SELECT d.dept_name, MAX(p.salary) AS max_salary FROM departments d JOIN professors p ON d.dept_id = p.dept_id WHERE p.is_tenured = TRUE GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "Which departments have deans whose salaries are higher than 150,000? Return exactly these columns in order: dept_name, first_name, last_name, salary.",
    "sql": "SELECT d.dept_name, p.first_name, p.last_name, p.salary FROM departments d JOIN professors p ON d.dean_id = p.prof_id WHERE p.salary > 150000;"
  },
  {
    "question": "Show the total budget and the total number of course codes under each department. Return exactly these columns in order: dept_name, budget, total_courses.",
    "sql": "SELECT d.dept_name, d.budget, COUNT(c.course_id) AS total_courses FROM departments d LEFT JOIN courses c ON d.dept_id = c.dept_id GROUP BY d.dept_id, d.dept_name, d.budget;"
  },
  {
    "question": "Identify students who have taken more than 5 courses with a grade of 'B+' or above. Return exactly these columns in order: first_name, last_name, good_grades.",
    "sql": "SELECT s.first_name, s.last_name, COUNT(e.enrollment_id) AS good_grades FROM students s JOIN enrollments e ON s.student_id = e.student_id WHERE e.grade IN ('A', 'A-', 'B+') GROUP BY s.student_id, s.first_name, s.last_name HAVING COUNT(e.enrollment_id) > 5;"
  },
  {
    "question": "Calculate the total number of credits taught by each professor. Return exactly these columns in order: first_name, last_name, total_credits_taught.",
    "sql": "SELECT p.first_name, p.last_name, SUM(c.credits) AS total_credits_taught FROM professors p JOIN offerings o ON p.prof_id = o.prof_id JOIN courses c ON o.course_id = c.course_id GROUP BY p.prof_id, p.first_name, p.last_name;"
  },
  {
    "question": "List the average department budget grouped by the building they are in. Return exactly these columns in order: building, avg_budget.",
    "sql": "SELECT building, AVG(budget) AS avg_budget FROM departments WHERE building IS NOT NULL GROUP BY building;"
  },
  {
    "question": "Find the total number of students in each study year who are enrolled in offerings taught by non-tenured professors. Return exactly these columns in order: year_of_study, student_count.",
    "sql": "SELECT s.year_of_study, COUNT(DISTINCT s.student_id) AS student_count FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN professors p ON o.prof_id = p.prof_id WHERE p.is_tenured = FALSE GROUP BY s.year_of_study;"
  },
  {
    "question": "Which departments have a higher total salary expense than their department budget? Return exactly these columns in order: dept_name, budget, total_salaries.",
    "sql": "SELECT d.dept_name, d.budget, SUM(p.salary) AS total_salaries FROM departments d JOIN professors p ON d.dept_id = p.dept_id GROUP BY d.dept_id, d.dept_name, d.budget HAVING SUM(p.salary) > d.budget;"
  },
  {
    "question": "Find the name of any professor whose salary is higher than the average professor salary across the entire university. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE salary > (SELECT AVG(salary) FROM professors);"
  },
  {
    "question": "Show all students who have a GPA higher than the average GPA of students in department ID 2. Return exactly these columns in order: first_name, last_name, gpa.",
    "sql": "SELECT first_name, last_name, gpa FROM students WHERE gpa > (SELECT AVG(gpa) FROM students WHERE major_dept_id = 2);"
  },
  {
    "question": "Identify courses that have never been offered. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE course_id NOT IN (SELECT DISTINCT course_id FROM offerings);"
  },
  {
    "question": "Find the student(s) with the absolute highest GPA in the university. Return exactly these columns in order: first_name, last_name, gpa.",
    "sql": "SELECT first_name, last_name, gpa FROM students WHERE gpa = (SELECT MAX(gpa) FROM students);"
  },
  {
    "question": "Which department has the highest budget? Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments WHERE budget = (SELECT MAX(budget) FROM departments);"
  },
  {
    "question": "Find professors who earn more than the dean of their department. Return exactly these columns in order: first_name, last_name, salary, dept_name.",
    "sql": "SELECT p.first_name, p.last_name, p.salary, d.dept_name FROM professors p JOIN departments d ON p.dept_id = d.dept_id WHERE p.salary > (SELECT salary FROM professors WHERE prof_id = d.dean_id);"
  },
  {
    "question": "List students who have a GPA that is strictly greater than the average GPA of students in their own major department. Return exactly these columns in order: first_name, last_name, gpa, dept_name.",
    "sql": "SELECT s1.first_name, s1.last_name, s1.gpa, d.dept_name FROM students s1 JOIN departments d ON s1.major_dept_id = d.dept_id WHERE s1.gpa > (SELECT AVG(s2.gpa) FROM students s2 WHERE s2.major_dept_id = s1.major_dept_id);"
  },
  {
    "question": "Find professors who have never taught any course offering. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE prof_id NOT IN (SELECT DISTINCT prof_id FROM offerings WHERE prof_id IS NOT NULL);"
  },
  {
    "question": "Get courses whose max enrollment is greater than the average max enrollment of all courses. Return exactly these columns in order: course_code, title, max_enrollment.",
    "sql": "SELECT course_code, title, max_enrollment FROM courses WHERE max_enrollment > (SELECT AVG(max_enrollment) FROM courses);"
  },
  {
    "question": "Show the department name and building of departments that have no students enrolled in any of their major courses. Return exactly these columns in order: dept_name, building.",
    "sql": "SELECT dept_name, building FROM departments WHERE dept_id NOT IN (SELECT DISTINCT major_dept_id FROM students WHERE major_dept_id IS NOT NULL);"
  },
  {
    "question": "Find the student(s) who enrolled first (minimum enrollment date). Return exactly these columns in order: first_name, last_name, enrollment_date.",
    "sql": "SELECT first_name, last_name, enrollment_date FROM students s JOIN enrollments e ON s.student_id = e.student_id WHERE e.enrollment_date = (SELECT MIN(enrollment_date) FROM enrollments);"
  },
  {
    "question": "Which professors earn less than the average salary of non-tenured professors? Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE salary < (SELECT AVG(salary) FROM professors WHERE is_tenured = FALSE);"
  },
  {
    "question": "Find courses that are offered in the 'Fall' semester but have never been offered in the 'Spring' semester. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT DISTINCT c.course_code, c.title FROM courses c JOIN offerings o ON c.course_id = o.course_id WHERE o.semester = 'Fall' AND c.course_id NOT IN (SELECT DISTINCT course_id FROM offerings WHERE semester = 'Spring');"
  },
  {
    "question": "Show details of the professor who has taught the most course offerings. Return all columns.",
    "sql": "SELECT * FROM professors WHERE prof_id = (SELECT prof_id FROM offerings GROUP BY prof_id ORDER BY COUNT(*) DESC LIMIT 1);"
  },
  {
    "question": "Find students who have taken all courses offered by department ID 3. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT s.first_name, s.last_name FROM students s WHERE NOT EXISTS (SELECT c.course_id FROM courses c WHERE c.dept_id = 3 AND c.course_id NOT IN (SELECT o.course_id FROM enrollments e JOIN offerings o ON e.offering_id = o.offering_id WHERE e.student_id = s.student_id));"
  },
  {
    "question": "Which department dean has been hired the longest ago (earliest hire date)? Return exactly these columns in order: dept_name, first_name, last_name, hire_date.",
    "sql": "SELECT dept_name, first_name, last_name, hire_date FROM departments d JOIN professors p ON d.dean_id = p.prof_id WHERE p.hire_date = (SELECT MIN(hire_date) FROM professors WHERE prof_id IN (SELECT DISTINCT dean_id FROM departments WHERE dean_id IS NOT NULL));"
  },
  {
    "question": "List students who received a grade higher than the average grade of the offering they were in (using numeric representation for grades: A=4.0, B=3.0, C=2.0, D=1.0, F=0.0). Return exactly these columns in order: first_name, last_name, grade, offering_id.",
    "sql": "SELECT s.first_name, s.last_name, e.grade, e.offering_id FROM enrollments e JOIN students s ON e.student_id = s.student_id WHERE (CASE e.grade WHEN 'A' THEN 4.0 WHEN 'A-' THEN 3.7 WHEN 'B+' THEN 3.3 WHEN 'B' THEN 3.0 WHEN 'B-' THEN 2.7 WHEN 'C+' THEN 2.3 WHEN 'C' THEN 2.0 WHEN 'D' THEN 1.0 ELSE 0.0 END) > (SELECT AVG(CASE grade WHEN 'A' THEN 4.0 WHEN 'A-' THEN 3.7 WHEN 'B+' THEN 3.3 WHEN 'B' THEN 3.0 WHEN 'B-' THEN 2.7 WHEN 'C+' THEN 2.3 WHEN 'C' THEN 2.0 WHEN 'D' THEN 1.0 ELSE 0.0 END) FROM enrollments e2 WHERE e2.offering_id = e.offering_id);"
  },
  {
    "question": "List the buildings that have departments with budgets above the average budget of all departments. Return exactly these columns in order: building.",
    "sql": "SELECT DISTINCT building FROM departments WHERE budget > (SELECT AVG(budget) FROM departments) AND building IS NOT NULL;"
  },
  {
    "question": "Find the student ID of students who have enrolled in more courses than student ID 15. Return exactly these columns in order: student_id, enroll_count.",
    "sql": "SELECT student_id, COUNT(*) AS enroll_count FROM enrollments GROUP BY student_id HAVING COUNT(*) > (SELECT COUNT(*) FROM enrollments WHERE student_id = 15);"
  },
  {
    "question": "Show the first name and last name of the highest-paid professor in each department. Return exactly these columns in order: first_name, last_name, salary, dept_name.",
    "sql": "SELECT p1.first_name, p1.last_name, p1.salary, d.dept_name FROM professors p1 JOIN departments d ON p1.dept_id = d.dept_id WHERE p1.salary = (SELECT MAX(p2.salary) FROM professors p2 WHERE p2.dept_id = p1.dept_id);"
  },
  {
    "question": "Find all courses that have a max enrollment value greater than the max enrollment of all courses in department 4. Return exactly these columns in order: title, max_enrollment.",
    "sql": "SELECT title, max_enrollment FROM courses WHERE max_enrollment > (SELECT MAX(max_enrollment) FROM courses WHERE dept_id = 4);"
  },
  {
    "question": "What is the title of the course that has the largest number of total student enrollments in the history of the university?",
    "sql": "SELECT title FROM courses WHERE course_id = (SELECT o.course_id FROM enrollments e JOIN offerings o ON e.offering_id = o.offering_id GROUP BY o.course_id ORDER BY COUNT(*) DESC LIMIT 1);"
  },
  {
    "question": "Identify students who have never enrolled in any course offering. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE student_id NOT IN (SELECT DISTINCT student_id FROM enrollments);"
  },
  {
    "question": "List the departments where the average professor salary is higher than the overall university average professor salary. Return exactly these columns in order: dept_name.",
    "sql": "SELECT d.dept_name FROM departments d JOIN professors p ON d.dept_id = p.dept_id GROUP BY d.dept_id, d.dept_name HAVING AVG(p.salary) > (SELECT AVG(salary) FROM professors);"
  },
  {
    "question": "Which students have a GPA lower than that of any student majoring in 'Physics'? Return exactly these columns in order: first_name, last_name, gpa.",
    "sql": "SELECT first_name, last_name, gpa FROM students WHERE gpa < (SELECT MIN(s.gpa) FROM students s JOIN departments d ON s.major_dept_id = d.dept_id WHERE d.dept_name = 'Physics');"
  },
  {
    "question": "Find the professors who have a salary that is within the top 10% of all salaries. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE salary >= (SELECT MIN(salary) FROM (SELECT salary FROM professors ORDER BY salary DESC LIMIT (SELECT CAST(COUNT(*) * 0.1 AS INT) FROM professors)));"
  },
  {
    "question": "Show all student details for those whose major department is located in the same building as the 'Humanities' department. Return exactly these columns in order: s.*.",
    "sql": "SELECT s.* FROM students s JOIN departments d ON s.major_dept_id = d.dept_id WHERE d.building = (SELECT building FROM departments WHERE dept_name = 'Humanities');"
  },
  {
    "question": "Find offerings that were taught by a professor who has a salary below the average professor salary in their own department. Return exactly these columns in order: offering_id, semester, year.",
    "sql": "SELECT o.offering_id, o.semester, o.year FROM offerings o JOIN professors p ON o.prof_id = p.prof_id WHERE p.salary < (SELECT AVG(p2.salary) FROM professors p2 WHERE p2.dept_id = p.dept_id);"
  },
  {
    "question": "Which students are enrolled in the same offerings as student ID 25? Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name FROM enrollments e JOIN students s ON e.student_id = s.student_id WHERE e.offering_id IN (SELECT offering_id FROM enrollments WHERE student_id = 25) AND s.student_id != 25;"
  },
  {
    "question": "Find the department dean details for the department with the lowest budget. Return all columns.",
    "sql": "SELECT * FROM professors WHERE prof_id = (SELECT dean_id FROM departments WHERE budget = (SELECT MIN(budget) FROM departments));"
  },
  {
    "question": "Show all courses that are offered in the same semester and year as 'CS101' was offered. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT DISTINCT c.course_code, c.title FROM courses c JOIN offerings o ON c.course_id = o.course_id WHERE (o.semester, o.year) IN (SELECT o2.semester, o2.year FROM offerings o2 JOIN courses c2 ON o2.course_id = c2.course_id WHERE c2.course_code = 'CS101');"
  },
  {
    "question": "Show the rank of professors based on their salary within each department. Return exactly these columns in order: first_name, last_name, dept_name, salary, salary_rank.",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name, p.salary, RANK() OVER (PARTITION BY p.dept_id ORDER BY p.salary DESC) AS salary_rank FROM professors p JOIN departments d ON p.dept_id = d.dept_id;"
  },
  {
    "question": "Find the top 3 students by GPA in each year of study using window functions. Return exactly these columns in order: student_id, first_name, last_name, year_of_study, gpa, rn.",
    "sql": "WITH ranked_students AS (SELECT student_id, first_name, last_name, year_of_study, gpa, ROW_NUMBER() OVER (PARTITION BY year_of_study ORDER BY gpa DESC) AS rn FROM students) SELECT first_name, last_name, year_of_study, gpa FROM ranked_students WHERE rn <= 3;"
  },
  {
    "question": "Display each student's name, their major, GPA, and the difference between their GPA and the average GPA of their major. Return exactly these columns in order: first_name, last_name, dept_name, gpa, gpa_difference.",
    "sql": "SELECT s.first_name, s.last_name, d.dept_name, s.gpa, s.gpa - AVG(s.gpa) OVER (PARTITION BY s.major_dept_id) AS gpa_difference FROM students s JOIN departments d ON s.major_dept_id = d.dept_id;"
  },
  {
    "question": "Write a query to list each department, its budget, and its rank based on the budget (highest budget is rank 1). Return exactly these columns in order: dept_name, budget, budget_rank.",
    "sql": "SELECT dept_name, budget, RANK() OVER (ORDER BY budget DESC) AS budget_rank FROM departments;"
  },
  {
    "question": "Find the cumulative salary of professors as they were hired within each department. Return exactly these columns in order: dept_name, first_name, last_name, hire_date, salary, cumulative_salary.",
    "sql": "SELECT d.dept_name, p.first_name, p.last_name, p.hire_date, p.salary, SUM(p.salary) OVER (PARTITION BY p.dept_id ORDER BY p.hire_date ASC) AS cumulative_salary FROM professors p JOIN departments d ON p.dept_id = d.dept_id;"
  },
  {
    "question": "List all courses with their titles, credits, and the percentage of credits they contribute to the total credits in their department. Return exactly these columns in order: title, dept_name, credits, credit_percentage.",
    "sql": "SELECT c.title, d.dept_name, c.credits, (CAST(c.credits AS REAL) / SUM(c.credits) OVER (PARTITION BY c.dept_id)) * 100 AS credit_percentage FROM courses c JOIN departments d ON c.dept_id = d.dept_id;"
  },
  {
    "question": "Identify students who have the same GPA as someone else in the same major department. Return exactly these columns in order: student_id, first_name, last_name, major_dept_id, gpa, gpa_count.",
    "sql": "WITH duplicate_gpas AS (SELECT student_id, first_name, last_name, major_dept_id, gpa, COUNT(*) OVER (PARTITION BY major_dept_id, gpa) AS gpa_count FROM students) SELECT first_name, last_name, gpa FROM duplicate_gpas WHERE gpa_count > 1;"
  },
  {
    "question": "Determine the percentage of professors in each department who are tenured. Return exactly these columns in order: dept_id, total_profs, tenured_count.",
    "sql": "WITH tenure_stats AS (SELECT dept_id, COUNT(*) AS total_profs, SUM(CASE WHEN is_tenured = TRUE THEN 1 ELSE 0 END) AS tenured_count FROM professors GROUP BY dept_id) SELECT d.dept_name, (CAST(t.tenured_count AS REAL) / t.total_profs) * 100 AS percent_tenured FROM tenure_stats t JOIN departments d ON t.dept_id = d.dept_id;"
  },
  {
    "question": "Retrieve a list of deans along with their department budgets, and find the running total of budgets managed by deans. Return exactly these columns in order: dept_name, first_name, last_name, budget, running_budget_total.",
    "sql": "SELECT d.dept_name, p.first_name, p.last_name, d.budget, SUM(d.budget) OVER (ORDER BY d.budget DESC) AS running_budget_total FROM departments d JOIN professors p ON d.dean_id = p.prof_id;"
  },
  {
    "question": "For each student, find their rank by GPA within the whole university, and also within their major department. Return exactly these columns in order: first_name, last_name, gpa, overall_rank, major_rank.",
    "sql": "SELECT s.first_name, s.last_name, s.gpa, RANK() OVER (ORDER BY s.gpa DESC) AS overall_rank, RANK() OVER (PARTITION BY s.major_dept_id ORDER BY s.gpa DESC) AS major_rank FROM students s;"
  },
  {
    "question": "Find the student who has the highest GPA in each major department using a CTE. Return exactly these columns in order: first_name, last_name, gpa, dept_name, rn.",
    "sql": "WITH highest_gpa_cte AS (SELECT s.first_name, s.last_name, s.gpa, d.dept_name, ROW_NUMBER() OVER (PARTITION BY s.major_dept_id ORDER BY s.gpa DESC) AS rn FROM students s JOIN departments d ON s.major_dept_id = d.dept_id) SELECT first_name, last_name, gpa, dept_name FROM highest_gpa_cte WHERE rn = 1;"
  },
  {
    "question": "Calculate the year-over-year enrollment numbers for each course. Return exactly these columns in order: course_code, title, year, enrollments_count.",
    "sql": "WITH annual_enrollments AS (SELECT c.course_code, c.title, o.year, COUNT(e.enrollment_id) AS enrollments_count FROM offerings o JOIN courses c ON o.course_id = c.course_id LEFT JOIN enrollments e ON o.offering_id = e.offering_id GROUP BY c.course_code, c.title, o.year) SELECT course_code, title, year, enrollments_count, LAG(enrollments_count, 1) OVER (PARTITION BY course_code ORDER BY year ASC) AS previous_year_enrollments FROM annual_enrollments;"
  },
  {
    "question": "List all department names, their budgets, and the budget of the department with the next highest budget. Return exactly these columns in order: dept_name, budget, next_higher_budget.",
    "sql": "SELECT dept_name, budget, LEAD(budget, 1) OVER (ORDER BY budget ASC) AS next_higher_budget FROM departments;"
  },
  {
    "question": "Which semesters had the highest number of student enrollments? Show semesters ranked by enrollment count. Return exactly these columns in order: semester, year, total_enrollments, enrollment_rank.",
    "sql": "SELECT o.semester, o.year, COUNT(e.enrollment_id) AS total_enrollments, RANK() OVER (ORDER BY COUNT(e.enrollment_id) DESC) AS enrollment_rank FROM enrollments e JOIN offerings o ON e.offering_id = o.offering_id GROUP BY o.semester, o.year;"
  },
  {
    "question": "Retrieve details of the second highest paid professor in each department. Return exactly these columns in order: p.*, rn.",
    "sql": "WITH ranked_professors AS (SELECT p.*, ROW_NUMBER() OVER (PARTITION BY p.dept_id ORDER BY p.salary DESC) AS rn FROM professors p) SELECT rp.first_name, rp.last_name, rp.salary, d.dept_name FROM ranked_professors rp JOIN departments d ON rp.dept_id = d.dept_id WHERE rp.rn = 2;"
  },
  {
    "question": "For each enrollment, calculate the days difference between the student's graduation date and the enrollment date. Return exactly these columns in order: first_name, last_name, enrollment_date, graduation_date, days_to_grad.",
    "sql": "SELECT s.first_name, s.last_name, e.enrollment_date, s.graduation_date, (JULIANDAY(s.graduation_date) - JULIANDAY(e.enrollment_date)) AS days_to_grad FROM enrollments e JOIN students s ON e.student_id = s.student_id WHERE s.graduation_date IS NOT NULL;"
  },
  {
    "question": "List each student and the difference between their GPA and the minimum GPA of students in the same year of study. Return exactly these columns in order: first_name, last_name, year_of_study, gpa, gpa_surplus.",
    "sql": "SELECT first_name, last_name, year_of_study, gpa, gpa - MIN(gpa) OVER (PARTITION BY year_of_study) AS gpa_surplus FROM students;"
  },
  {
    "question": "Show the list of deans, their department budgets, and the percentage of the total university budget their department represents. Return exactly these columns in order: first_name, last_name, dept_name, budget, budget).",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name, d.budget, (d.budget / (SELECT SUM(budget) FROM departments)) * 100 AS budget_percentage FROM departments d JOIN professors p ON d.dean_id = p.prof_id;"
  },
  {
    "question": "Find the total salary of tenured professors as a proportion of the total salary of all professors in each department. Return exactly these columns in order: dept_id, total_sal, tenured_sal.",
    "sql": "WITH dept_salaries AS (SELECT dept_id, SUM(salary) AS total_sal, SUM(CASE WHEN is_tenured = TRUE THEN salary ELSE 0 END) AS tenured_sal FROM professors GROUP BY dept_id) SELECT d.dept_name, (CAST(ds.tenured_sal AS REAL) / ds.total_sal) * 100 AS tenured_salary_ratio FROM dept_salaries ds JOIN departments d ON ds.dept_id = d.dept_id;"
  },
  {
    "question": "List all departments and display 'Large Budget' if budget is above 1,000,000, 'Medium Budget' if between 500,000 and 1,000,000, and 'Small Budget' otherwise. Return exactly these columns in order: dept_name, budget, budget_category.",
    "sql": "SELECT dept_name, budget, CASE WHEN budget > 1000000 THEN 'Large Budget' WHEN budget BETWEEN 500000 AND 1000000 THEN 'Medium Budget' ELSE 'Small Budget' END AS budget_category FROM departments;"
  },
  {
    "question": "Show the list of students with their GPAs, and classify them into 'First Class' (GPA >= 3.5), 'Second Class' (GPA BETWEEN 3.0 AND 3.49), and 'Pass' (GPA < 3.0). Return exactly these columns in order: first_name, last_name, gpa, class_rating.",
    "sql": "SELECT first_name, last_name, gpa, CASE WHEN gpa >= 3.5 THEN 'First Class' WHEN gpa BETWEEN 3.0 AND 3.49 THEN 'Second Class' ELSE 'Pass' END AS class_rating FROM students;"
  },
  {
    "question": "Retrieve a list of courses along with the student headcount enrolled in their most recent offering. Return exactly these columns in order: course_id, offering_id, rn.",
    "sql": "WITH recent_offerings AS (SELECT course_id, offering_id, ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY year DESC, CASE semester WHEN 'Fall' THEN 3 WHEN 'Spring' THEN 2 WHEN 'Summer' THEN 1 END DESC) AS rn FROM offerings) SELECT c.course_code, c.title, COUNT(e.enrollment_id) AS enrollment_count FROM recent_offerings ro JOIN courses c ON ro.course_id = c.course_id JOIN enrollments e ON ro.offering_id = e.offering_id WHERE ro.rn = 1 GROUP BY c.course_id, c.course_code, c.title;"
  },
  {
    "question": "Get a list of all professors and count how many active students they teach in the Fall semester of 2024. Return exactly these columns in order: first_name, last_name, student_count.",
    "sql": "SELECT p.first_name, p.last_name, COUNT(DISTINCT e.student_id) AS student_count FROM professors p JOIN offerings o ON p.prof_id = o.prof_id JOIN enrollments e ON o.offering_id = e.offering_id WHERE o.semester = 'Fall' AND o.year = 2024 GROUP BY p.prof_id, p.first_name, p.last_name;"
  },
  {
    "question": "Determine which students are taking courses from departments other than their own major department, listing the student's name and the non-major department name. Return exactly these columns in order: first_name, last_name, non_major_dept.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name, d.dept_name AS non_major_dept FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id JOIN departments d ON c.dept_id = d.dept_id WHERE s.major_dept_id != c.dept_id;"
  },
  {
    "question": "Find the total credit hours enrolled by students who are currently in their first year of study. Return exactly these columns in order: first_year_credits.",
    "sql": "SELECT SUM(c.credits) AS first_year_credits FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id WHERE s.year_of_study = 1;"
  },
  {
    "question": "Identify departments where the number of professors is greater than the number of courses offered. Return exactly these columns in order: dept_id, prof_count.",
    "sql": "WITH prof_counts AS (SELECT dept_id, COUNT(*) AS prof_count FROM professors GROUP BY dept_id), course_counts AS (SELECT dept_id, COUNT(*) AS course_count FROM courses GROUP BY dept_id) SELECT d.dept_name FROM departments d JOIN prof_counts pc ON d.dept_id = pc.dept_id JOIN course_counts cc ON d.dept_id = cc.dept_id WHERE pc.prof_count > cc.course_count;"
  },
  {
    "question": "Find the courses which had a higher enrollment in 2024 than their max enrollment limit allowed (over-enrollment). Return exactly these columns in order: course_code, title, max_enrollment, actual_enrollment.",
    "sql": "SELECT c.course_code, c.title, c.max_enrollment, COUNT(e.enrollment_id) AS actual_enrollment FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN enrollments e ON o.offering_id = e.offering_id WHERE o.year = 2024 GROUP BY o.offering_id, c.course_code, c.title, c.max_enrollment HAVING COUNT(e.enrollment_id) > c.max_enrollment;"
  },
  {
    "question": "Show a matrix-like output of total students in each department graduating in 2025, 2026, and 2027. Return exactly these columns in order: dept_name, grad_2025, grad_2026, grad_2027.",
    "sql": "SELECT d.dept_name, SUM(CASE WHEN strftime('%Y', s.graduation_date) = '2025' THEN 1 ELSE 0 END) AS grad_2025, SUM(CASE WHEN strftime('%Y', s.graduation_date) = '2026' THEN 1 ELSE 0 END) AS grad_2026, SUM(CASE WHEN strftime('%Y', s.graduation_date) = '2027' THEN 1 ELSE 0 END) AS grad_2027 FROM departments d JOIN students s ON d.dept_id = s.major_dept_id GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "Find the average salary of professors who teach courses that are worth 4 credits. Return exactly these columns in order: average_salary.",
    "sql": "SELECT AVG(p.salary) AS average_salary FROM professors p JOIN offerings o ON p.prof_id = o.prof_id JOIN courses c ON o.course_id = c.course_id WHERE c.credits = 4;"
  },
  {
    "question": "For each student, display their first and last name, their major department, and the difference in budget between their department and the department with the largest budget. Return exactly these columns in order: first_name, last_name, dept_name, budget).",
    "sql": "SELECT s.first_name, s.last_name, d.dept_name, (SELECT MAX(budget) FROM departments) - d.budget AS budget_gap FROM students s JOIN departments d ON s.major_dept_id = d.dept_id;"
  },
  {
    "question": "Which offerings have an enrollment count that is lower than 10% of their course's max enrollment capacity? Return exactly these columns in order: offering_id, title, current_enrollment, max_enrollment.",
    "sql": "SELECT o.offering_id, c.title, COUNT(e.enrollment_id) AS current_enrollment, c.max_enrollment FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN enrollments e ON o.offering_id = e.offering_id GROUP BY o.offering_id, c.title, c.max_enrollment HAVING COUNT(e.enrollment_id) < (c.max_enrollment * 0.1);"
  },
  {
    "question": "List the names of professors who have taught courses in every semester (Fall, Spring, Summer) at some point. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT p.first_name, p.last_name FROM professors p JOIN offerings o ON p.prof_id = o.prof_id GROUP BY p.prof_id, p.first_name, p.last_name HAVING COUNT(DISTINCT o.semester) = 3;"
  },
  {
    "question": "Calculate the average GPA of students enrolled in offerings taught by deans. Return exactly these columns in order: avg_gpa_under_dean.",
    "sql": "SELECT AVG(s.gpa) AS avg_gpa_under_dean FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN departments d ON o.prof_id = d.dean_id;"
  },
  {
    "question": "Find students who got an 'A' in a course taught by their major department's dean. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN departments d ON s.major_dept_id = d.dept_id WHERE e.grade = 'A' AND o.prof_id = d.dean_id;"
  },
  {
    "question": "Which professors teach courses in buildings other than the building where their own department is located? Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT DISTINCT p.first_name, p.last_name FROM professors p JOIN departments pd ON p.dept_id = pd.dept_id JOIN offerings o ON p.prof_id = o.prof_id JOIN courses c ON o.course_id = c.course_id JOIN departments cd ON c.dept_id = cd.dept_id WHERE pd.building != cd.building;"
  },
  {
    "question": "List all departments and show the student-to-professor ratio (students majoring in dept / professors in dept). Return exactly these columns in order: major_dept_id, s_count.",
    "sql": "WITH student_counts AS (SELECT major_dept_id, COUNT(*) AS s_count FROM students GROUP BY major_dept_id), prof_counts AS (SELECT dept_id, COUNT(*) AS p_count FROM professors GROUP BY dept_id) SELECT d.dept_name, CAST(COALESCE(sc.s_count, 0) AS REAL) / COALESCE(pc.p_count, 1) AS student_prof_ratio FROM departments d LEFT JOIN student_counts sc ON d.dept_id = sc.major_dept_id LEFT JOIN prof_counts pc ON d.dept_id = pc.dept_id;"
  },
  {
    "question": "Find all enrollments of students whose GPA is within the top 5% of all students. Return all columns.",
    "sql": "SELECT * FROM enrollments WHERE student_id IN (SELECT student_id FROM students WHERE gpa >= (SELECT MIN(gpa) FROM (SELECT gpa FROM students ORDER BY gpa DESC LIMIT (SELECT CAST(COUNT(*) * 0.05 AS INT) FROM students))));"
  },
  {
    "question": "For each student, display their name, major, and a list of all grades they have received in a single comma-separated string. Return exactly these columns in order: first_name, last_name, dept_name, grades_list.",
    "sql": "SELECT s.first_name, s.last_name, d.dept_name, GROUP_CONCAT(e.grade) AS grades_list FROM students s JOIN departments d ON s.major_dept_id = d.dept_id LEFT JOIN enrollments e ON s.student_id = e.student_id GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;"
  },
  {
    "question": "Identify students who have failed (grade 'F') or withdrawn ('W') from the same course more than once. Return exactly these columns in order: first_name, last_name, title, attempts.",
    "sql": "SELECT s.first_name, s.last_name, c.title, COUNT(*) AS attempts FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id WHERE e.grade IN ('F', 'W') GROUP BY s.student_id, c.course_id HAVING COUNT(*) > 1;"
  },
  {
    "question": "Find all departments that have a budget higher than the average budget of departments located in the same building. Return exactly these columns in order: dept_name, building, budget.",
    "sql": "SELECT d1.dept_name, d1.building, d1.budget FROM departments d1 WHERE d1.budget > (SELECT AVG(d2.budget) FROM departments d2 WHERE d2.building = d1.building);"
  },
  {
    "question": "Identify professors who have taught at least one course every year since 2022. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT p.first_name, p.last_name FROM professors p JOIN offerings o ON p.prof_id = o.prof_id WHERE o.year >= 2022 GROUP BY p.prof_id, p.first_name, p.last_name HAVING COUNT(DISTINCT o.year) = (SELECT COUNT(DISTINCT year) FROM offerings WHERE year >= 2022);"
  },
  {
    "question": "Find the maximum salary for tenured and non-tenured professors across each building where their departments are located. Return exactly these columns in order: building, is_tenured, max_salary.",
    "sql": "SELECT d.building, p.is_tenured, MAX(p.salary) AS max_salary FROM professors p JOIN departments d ON p.dept_id = d.dept_id WHERE d.building IS NOT NULL GROUP BY d.building, p.is_tenured;"
  },
  {
    "question": "Show students' first and last names and their cumulative GPA rank within their department, showing only those with a rank of 1 or 2. Return exactly these columns in order: first_name, last_name, gpa, dept_name, rk.",
    "sql": "WITH ranked_students AS (SELECT s.first_name, s.last_name, s.gpa, d.dept_name, RANK() OVER (PARTITION BY s.major_dept_id ORDER BY s.gpa DESC) AS rk FROM students s JOIN departments d ON s.major_dept_id = d.dept_id) SELECT first_name, last_name, gpa, dept_name, rk FROM ranked_students WHERE rk <= 2;"
  },
  {
    "question": "Find all student details for those whose major department name contains 'Engineering' and who have a GPA above 3.5. Return exactly these columns in order: s.*.",
    "sql": "SELECT s.* FROM students s JOIN departments d ON s.major_dept_id = d.dept_id WHERE d.dept_name LIKE '%Engineering%' AND s.gpa > 3.5;"
  },
  {
    "question": "List all courses with their titles and codes, ordered by credit hours descending and then by title alphabetically. Return exactly these columns in order: course_code, title, credits.",
    "sql": "SELECT course_code, title, credits FROM courses ORDER BY credits DESC, title ASC;"
  },
  {
    "question": "Which professors earn more than 100,000 but are not yet tenured? Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE salary > 100000 AND is_tenured = FALSE;"
  },
  {
    "question": "Retrieve the first name, last name, and graduation date of all students who will graduate after June 2025. Return exactly these columns in order: first_name, last_name, graduation_date.",
    "sql": "SELECT first_name, last_name, graduation_date FROM students WHERE graduation_date > '2025-06-30';"
  },
  {
    "question": "Find all offerings taught by the professor with ID 8. Return exactly these columns in order: offering_id, course_id, semester, year.",
    "sql": "SELECT offering_id, course_id, semester, year FROM offerings WHERE prof_id = 8;"
  },
  {
    "question": "List all students whose GPAs are in the range of 3.8 to 4.0, ordered by GPA descending. Return exactly these columns in order: student_id, first_name, last_name, gpa.",
    "sql": "SELECT student_id, first_name, last_name, gpa FROM students WHERE gpa BETWEEN 3.8 AND 4.0 ORDER BY gpa DESC;"
  },
  {
    "question": "Retrieve the building and budget for the department named 'Physics'.",
    "sql": "SELECT building, budget FROM departments WHERE dept_name = 'Physics';"
  },
  {
    "question": "Find all courses belonging to department ID 2 that are worth exactly 3 credits. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE dept_id = 2 AND credits = 3;"
  },
  {
    "question": "Show all student enrollments that occurred in 2024. Return all columns.",
    "sql": "SELECT * FROM enrollments WHERE enrollment_date BETWEEN '2024-01-01' AND '2024-12-31';"
  },
  {
    "question": "Which professors have 'John' as their first name and are tenured? Return exactly these columns in order: prof_id, first_name, last_name.",
    "sql": "SELECT prof_id, first_name, last_name FROM professors WHERE first_name = 'John' AND is_tenured = TRUE;"
  },
  {
    "question": "Find all departments that are in building 'East Wing' or 'West Wing'. Return exactly these columns in order: dept_name, building.",
    "sql": "SELECT dept_name, building FROM departments WHERE building IN ('East Wing', 'West Wing');"
  },
  {
    "question": "List the details of students in their 3rd or 4th year with a GPA below 2.5. Return exactly these columns in order: student_id, first_name, last_name, gpa, year_of_study.",
    "sql": "SELECT student_id, first_name, last_name, gpa, year_of_study FROM students WHERE year_of_study IN (3, 4) AND gpa < 2.5;"
  },
  {
    "question": "Retrieve the first and last names of students who graduated on '2025-05-18'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE graduation_date = '2025-05-18';"
  },
  {
    "question": "List all distinct course codes offered in the Fall semester of any year. Return exactly these columns in order: course_code.",
    "sql": "SELECT DISTINCT c.course_code FROM offerings o JOIN courses c ON o.course_id = c.course_id WHERE o.semester = 'Fall';"
  },
  {
    "question": "Find professors who have a salary of less than 50,000 or greater than 150,000. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE salary < 50000 OR salary > 150000;"
  },
  {
    "question": "List the course code and credit hours for all courses with credits not equal to 3. Return exactly these columns in order: course_code, credits.",
    "sql": "SELECT course_code, credits FROM courses WHERE credits != 3;"
  },
  {
    "question": "Find all enrollments that received a grade of 'B', 'B-', 'C+', or 'C'. Return exactly these columns in order: enrollment_id, grade.",
    "sql": "SELECT enrollment_id, grade FROM enrollments WHERE grade IN ('B', 'B-', 'C+', 'C');"
  },
  {
    "question": "Show the details of the department with budget exactly equal to 500,000. Return all columns.",
    "sql": "SELECT * FROM departments WHERE budget = 500000;"
  },
  {
    "question": "Get all distinct major department IDs declared by students. Return exactly these columns in order: major_dept_id.",
    "sql": "SELECT DISTINCT major_dept_id FROM students WHERE major_dept_id IS NOT NULL;"
  },
  {
    "question": "List students whose last names start with 'A' or 'B'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE last_name LIKE 'A%' OR last_name LIKE 'B%';"
  },
  {
    "question": "Retrieve details of all offerings for the year 2026, sorted by semester. Return all columns.",
    "sql": "SELECT * FROM offerings WHERE year = 2026 ORDER BY semester;"
  },
  {
    "question": "Show all courses that have a maximum enrollment of more than 100 students, ordered by capacity descending. Return exactly these columns in order: course_code, title, max_enrollment.",
    "sql": "SELECT course_code, title, max_enrollment FROM courses WHERE max_enrollment > 100 ORDER BY max_enrollment DESC;"
  },
  {
    "question": "Find all students who have a major department declared. Return exactly these columns in order: first_name, last_name, major_dept_id.",
    "sql": "SELECT first_name, last_name, major_dept_id FROM students WHERE major_dept_id IS NOT NULL;"
  },
  {
    "question": "List the names of professors hired in the range of 2015 to 2020. Return exactly these columns in order: first_name, last_name, hire_date.",
    "sql": "SELECT first_name, last_name, hire_date FROM professors WHERE hire_date BETWEEN '2015-01-01' AND '2020-12-31';"
  },
  {
    "question": "Show all student enrollments that did not receive a grade of 'F'. Return all columns.",
    "sql": "SELECT * FROM enrollments WHERE grade != 'F' OR grade IS NULL;"
  },
  {
    "question": "Identify departments with budgets between 750,000 and 1,250,000. Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments WHERE budget BETWEEN 750000 AND 1250000;"
  },
  {
    "question": "What courses are offered with maximum enrollment limits of exactly 30, 40, or 50? Return exactly these columns in order: course_code, title, max_enrollment.",
    "sql": "SELECT course_code, title, max_enrollment FROM courses WHERE max_enrollment IN (30, 40, 50);"
  },
  {
    "question": "Get a list of all distinct years in which offerings were made. Return exactly these columns in order: year.",
    "sql": "SELECT DISTINCT year FROM offerings;"
  },
  {
    "question": "Show details of the 10 students with the lowest GPAs. Return all columns.",
    "sql": "SELECT * FROM students ORDER BY gpa ASC LIMIT 10;"
  },
  {
    "question": "Find professors who have a first name starting with 'S'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE first_name LIKE 'S%';"
  },
  {
    "question": "Retrieve all course offerings that are taught during the Summer semester of 2024. Return all columns.",
    "sql": "SELECT * FROM offerings WHERE semester = 'Summer' AND year = 2024;"
  },
  {
    "question": "List all departments in 'Science Center' building, ordered by budget descending. Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments WHERE building = 'Science Center' ORDER BY budget DESC;"
  },
  {
    "question": "Find the student with last name 'Williams' and first name 'David'. Return exactly these columns in order: student_id, year_of_study, gpa.",
    "sql": "SELECT student_id, year_of_study, gpa FROM students WHERE last_name = 'Williams' AND first_name = 'David';"
  },
  {
    "question": "List all distinct courses that have at least one offering. Return exactly these columns in order: course_id.",
    "sql": "SELECT DISTINCT course_id FROM offerings;"
  },
  {
    "question": "Show all enrollments for student ID 123. Return all columns.",
    "sql": "SELECT * FROM enrollments WHERE student_id = 123;"
  },
  {
    "question": "Find departments that have a budget less than 100,000. Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments WHERE budget < 100000;"
  },
  {
    "question": "Find all courses taught in the year 2022 along with their professor's first and last name. Return exactly these columns in order: title, first_name, last_name.",
    "sql": "SELECT DISTINCT c.title, p.first_name, p.last_name FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN professors p ON o.prof_id = p.prof_id WHERE o.year = 2022;"
  },
  {
    "question": "Retrieve the first name, last name, and grade of students enrolled in course offering 12. Return exactly these columns in order: first_name, last_name, grade.",
    "sql": "SELECT s.first_name, s.last_name, e.grade FROM enrollments e JOIN students s ON e.student_id = s.student_id WHERE e.offering_id = 12;"
  },
  {
    "question": "List all courses with their titles and the department names they belong to. Return exactly these columns in order: title, dept_name.",
    "sql": "SELECT c.title, d.dept_name FROM courses c JOIN departments d ON c.dept_id = d.dept_id;"
  },
  {
    "question": "Which students are majoring in a department located in 'Main Hall' and have a GPA above 3.6? Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT s.first_name, s.last_name FROM students s JOIN departments d ON s.major_dept_id = d.dept_id WHERE d.building = 'Main Hall' AND s.gpa > 3.6;"
  },
  {
    "question": "Show the list of offerings including course codes and titles, taught by Professor 'Jane Doe'. Return exactly these columns in order: course_code, title, semester, year.",
    "sql": "SELECT c.course_code, c.title, o.semester, o.year FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN professors p ON o.prof_id = p.prof_id WHERE p.first_name = 'Jane' AND p.last_name = 'Doe';"
  },
  {
    "question": "Retrieve a list of students majoring in the department with dean ID 5. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT s.first_name, s.last_name FROM students s JOIN departments d ON s.major_dept_id = d.dept_id WHERE d.dean_id = 5;"
  },
  {
    "question": "List all courses offered in 2024 and the names of the departments offering them. Return exactly these columns in order: title, dept_name.",
    "sql": "SELECT DISTINCT c.title, d.dept_name FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN departments d ON c.dept_id = d.dept_id WHERE o.year = 2024;"
  },
  {
    "question": "Show the first name, last name, and department name of professors whose hire date is after '2018-01-01'. Return exactly these columns in order: first_name, last_name, dept_name.",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name FROM professors p JOIN departments d ON p.dept_id = d.dept_id WHERE p.hire_date > '2018-01-01';"
  },
  {
    "question": "List the titles of all courses that student ID 45 has enrolled in. Return exactly these columns in order: title.",
    "sql": "SELECT c.title FROM enrollments e JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id WHERE e.student_id = 45;"
  },
  {
    "question": "Identify students who are enrolled in 'Fall 2023' and got an 'A' grade. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT s.first_name, s.last_name FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id WHERE o.semester = 'Fall' AND o.year = 2023 AND e.grade = 'A';"
  },
  {
    "question": "Find the names of students and their major departments, including those students without a declared major. Return exactly these columns in order: first_name, last_name, dept_name.",
    "sql": "SELECT s.first_name, s.last_name, d.dept_name FROM students s LEFT JOIN departments d ON s.major_dept_id = d.dept_id;"
  },
  {
    "question": "List all department names and their dean's salary. Return exactly these columns in order: dept_name, first_name, last_name, salary.",
    "sql": "SELECT d.dept_name, p.first_name, p.last_name, p.salary FROM departments d JOIN professors p ON d.dean_id = p.prof_id;"
  },
  {
    "question": "Retrieve courses along with their offering semesters and years, including courses that have never been offered. Return exactly these columns in order: title, semester, year.",
    "sql": "SELECT c.title, o.semester, o.year FROM courses c LEFT JOIN offerings o ON c.course_id = o.course_id;"
  },
  {
    "question": "Show the first name, last name, and building of professors who are tenured. Return exactly these columns in order: first_name, last_name, building.",
    "sql": "SELECT p.first_name, p.last_name, d.building FROM professors p JOIN departments d ON p.dept_id = d.dept_id WHERE p.is_tenured = TRUE;"
  },
  {
    "question": "Which students are enrolled in offerings taught by a professor from department ID 3? Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN professors p ON o.prof_id = p.prof_id WHERE p.dept_id = 3;"
  },
  {
    "question": "Retrieve a list of students majoring in 'Chemistry' who are graduating in '2026-05-20'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT s.first_name, s.last_name FROM students s JOIN departments d ON s.major_dept_id = d.dept_id WHERE d.dept_name = 'Chemistry' AND s.graduation_date = '2026-05-20';"
  },
  {
    "question": "Get details of all course offerings taught by non-tenured professors in 2025. Return exactly these columns in order: title, last_name, semester.",
    "sql": "SELECT c.title, p.last_name, o.semester FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN professors p ON o.prof_id = p.prof_id WHERE p.is_tenured = FALSE AND o.year = 2025;"
  },
  {
    "question": "Identify students who have enrolled in any course offering with credits equal to 4. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id WHERE c.credits = 4;"
  },
  {
    "question": "List all departments, and if they have any professors, list the names of those professors. Return exactly these columns in order: dept_name, first_name, last_name.",
    "sql": "SELECT d.dept_name, p.first_name, p.last_name FROM departments d LEFT JOIN professors p ON d.dept_id = p.dept_id;"
  },
  {
    "question": "Find the student names and offering years for all enrollments with a grade of 'D' or 'F'. Return exactly these columns in order: first_name, last_name, year, grade.",
    "sql": "SELECT s.first_name, s.last_name, o.year, e.grade FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id WHERE e.grade IN ('D', 'F');"
  },
  {
    "question": "Retrieve courses whose department building is 'West Hall' and max enrollment is over 50. Return exactly these columns in order: title, dept_name.",
    "sql": "SELECT c.title, d.dept_name FROM courses c JOIN departments d ON c.dept_id = d.dept_id WHERE d.building = 'West Hall' AND c.max_enrollment > 50;"
  },
  {
    "question": "List all offerings, showing course titles and professor hire dates. Return exactly these columns in order: title, first_name, last_name, hire_date.",
    "sql": "SELECT c.title, p.first_name, p.last_name, p.hire_date FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN professors p ON o.prof_id = p.prof_id;"
  },
  {
    "question": "Show the first name, last name, and department of students who have enrolled in offerings of 'CS202'. Return exactly these columns in order: first_name, last_name, dept_name.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name, d.dept_name FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN departments d ON s.major_dept_id = d.dept_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id WHERE c.course_code = 'CS202';"
  },
  {
    "question": "Get details of departments including names and budgets, along with the total number of students majoring in them. Return exactly these columns in order: dept_name, budget, student_count.",
    "sql": "SELECT d.dept_name, d.budget, COUNT(s.student_id) AS student_count FROM departments d LEFT JOIN students s ON d.dept_id = s.major_dept_id GROUP BY d.dept_id, d.dept_name, d.budget;"
  },
  {
    "question": "List deans whose departments have a budget lower than 750,000. Return exactly these columns in order: first_name, last_name, dept_name, budget.",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name, d.budget FROM departments d JOIN professors p ON d.dean_id = p.prof_id WHERE d.budget < 750000;"
  },
  {
    "question": "Which course offerings are taught by deans, showing course title, dean name, and offering year? Return exactly these columns in order: title, first_name, last_name, year.",
    "sql": "SELECT c.title, p.first_name, p.last_name, o.year FROM offerings o JOIN courses c ON o.course_id = c.course_id JOIN departments d ON c.dept_id = d.dept_id JOIN professors p ON d.dean_id = p.prof_id WHERE o.prof_id = d.dean_id;"
  },
  {
    "question": "Show all students enrolled in courses taught by Professor 'Michael Brown' in 'Spring 2024'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN professors p ON o.prof_id = p.prof_id WHERE p.first_name = 'Michael' AND p.last_name = 'Brown' AND o.semester = 'Spring' AND o.year = 2024;"
  },
  {
    "question": "For each student enrollment, list student full name, course code, grade, and department name of the course. Return exactly these columns in order: first_name, last_name, course_code, grade, dept_name.",
    "sql": "SELECT s.first_name, s.last_name, c.course_code, e.grade, d.dept_name FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id JOIN departments d ON c.dept_id = d.dept_id;"
  },
  {
    "question": "Retrieve all students who are in their 4th year and are enrolled in courses managed by their own major department. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id WHERE s.year_of_study = 4 AND s.major_dept_id = c.dept_id;"
  },
  {
    "question": "Identify students who have enrolled in 'Summer 2023' offerings, and show their GPA. Return exactly these columns in order: first_name, last_name, gpa.",
    "sql": "SELECT s.first_name, s.last_name, s.gpa FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id WHERE o.semester = 'Summer' AND o.year = 2023;"
  },
  {
    "question": "Which departments have at least one professor whose salary is exactly 120,000? Return exactly these columns in order: dept_name.",
    "sql": "SELECT DISTINCT d.dept_name FROM departments d JOIN professors p ON d.dept_id = p.dept_id WHERE p.salary = 120000;"
  },
  {
    "question": "Show all student names and enrollments where the grade is an 'A-' or 'B+'. Return exactly these columns in order: first_name, last_name, grade, enrollment_date.",
    "sql": "SELECT s.first_name, s.last_name, e.grade, e.enrollment_date FROM enrollments e JOIN students s ON e.student_id = s.student_id WHERE e.grade IN ('A-', 'B+');"
  },
  {
    "question": "Find the average salary of professors who are deans compared to those who are not. Return exactly these columns in order: status, average_salary.",
    "sql": "SELECT CASE WHEN d.dean_id IS NOT NULL THEN 'Dean' ELSE 'Not Dean' END AS status, AVG(p.salary) AS average_salary FROM professors p LEFT JOIN departments d ON p.prof_id = d.dean_id GROUP BY status;"
  },
  {
    "question": "List student names and their major departments, including majors that have no students (show nulls for student names). Return exactly these columns in order: dept_name, first_name, last_name.",
    "sql": "SELECT d.dept_name, s.first_name, s.last_name FROM departments d LEFT JOIN students s ON d.dept_id = s.major_dept_id;"
  },
  {
    "question": "Find the number of courses and average max enrollment limit for each major department. Return exactly these columns in order: dept_name, course_count, average_max_enrollment.",
    "sql": "SELECT d.dept_name, COUNT(c.course_id) AS course_count, AVG(c.max_enrollment) AS average_max_enrollment FROM departments d JOIN courses c ON d.dept_id = c.dept_id GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "What is the total department budget and student count for each building? Return exactly these columns in order: building, total_budget, student_count.",
    "sql": "SELECT d.building, SUM(d.budget) AS total_budget, COUNT(s.student_id) AS student_count FROM departments d LEFT JOIN students s ON d.dept_id = s.major_dept_id WHERE d.building IS NOT NULL GROUP BY d.building;"
  },
  {
    "question": "For each grade, list the grade and the average GPA of students who received that grade. Return exactly these columns in order: grade, average_gpa.",
    "sql": "SELECT e.grade, AVG(s.gpa) AS average_gpa FROM enrollments e JOIN students s ON e.student_id = s.student_id GROUP BY e.grade;"
  },
  {
    "question": "Find the number of non-tenured professors in each department. Return exactly these columns in order: dept_name, non_tenured_count.",
    "sql": "SELECT d.dept_name, COUNT(p.prof_id) AS non_tenured_count FROM departments d LEFT JOIN professors p ON d.dept_id = p.dept_id AND p.is_tenured = FALSE GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "Find the average GPA and student count for each department offering courses, showing only departments with an average GPA above 3.2. Return exactly these columns in order: dept_name, average_gpa, total_students.",
    "sql": "SELECT d.dept_name, AVG(s.gpa) AS average_gpa, COUNT(s.student_id) AS total_students FROM departments d JOIN students s ON d.dept_id = s.major_dept_id GROUP BY d.dept_id, d.dept_name HAVING AVG(s.gpa) > 3.2;"
  },
  {
    "question": "Show the number of tenured professors hired in each year. Return exactly these columns in order: hire_year, tenured_count.",
    "sql": "SELECT strftime('%Y', hire_date) AS hire_year, COUNT(*) AS tenured_count FROM professors WHERE is_tenured = TRUE GROUP BY hire_year;"
  },
  {
    "question": "Find the total, maximum, and minimum student GPA for each major department. Return exactly these columns in order: dept_name, sum_gpa, max_gpa, min_gpa.",
    "sql": "SELECT d.dept_name, SUM(s.gpa) AS sum_gpa, MAX(s.gpa) AS max_gpa, MIN(s.gpa) AS min_gpa FROM departments d JOIN students s ON d.dept_id = s.major_dept_id GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "What is the total salary expenditure on tenured professors in each department? Return exactly these columns in order: dept_name, tenured_salary_total.",
    "sql": "SELECT d.dept_name, SUM(p.salary) AS tenured_salary_total FROM departments d JOIN professors p ON d.dept_id = p.dept_id WHERE p.is_tenured = TRUE GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "For each student, find the total number of credits they have completed with a grade of 'C' or better. Return exactly these columns in order: student_id, first_name, last_name, credits_completed.",
    "sql": "SELECT s.student_id, s.first_name, s.last_name, SUM(c.credits) AS credits_completed FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id WHERE e.grade NOT IN ('D', 'F', 'W') GROUP BY s.student_id, s.first_name, s.last_name;"
  },
  {
    "question": "Identify departments with total budgets of more than 2,000,000 and having more than 10 professors. Return exactly these columns in order: dept_name, budget, prof_count.",
    "sql": "SELECT d.dept_name, d.budget, COUNT(p.prof_id) AS prof_count FROM departments d JOIN professors p ON d.dept_id = p.dept_id GROUP BY d.dept_id, d.dept_name, d.budget HAVING d.budget > 2000000 AND COUNT(p.prof_id) > 10;"
  },
  {
    "question": "Find the average maximum enrollment limit for each building's departments. Return exactly these columns in order: building, average_max_enrollment.",
    "sql": "SELECT d.building, AVG(c.max_enrollment) AS average_max_enrollment FROM departments d JOIN courses c ON d.dept_id = c.dept_id WHERE d.building IS NOT NULL GROUP BY d.building;"
  },
  {
    "question": "For each semester and year, show the total number of student enrollments. Return exactly these columns in order: semester, year, total_enrollments.",
    "sql": "SELECT o.semester, o.year, COUNT(e.enrollment_id) AS total_enrollments FROM offerings o LEFT JOIN enrollments e ON o.offering_id = e.offering_id GROUP BY o.semester, o.year;"
  },
  {
    "question": "Show the list of professors and the maximum course credits of any course they have taught. Return exactly these columns in order: first_name, last_name, max_course_credits.",
    "sql": "SELECT p.first_name, p.last_name, MAX(c.credits) AS max_course_credits FROM professors p JOIN offerings o ON p.prof_id = o.prof_id JOIN courses c ON o.course_id = c.course_id GROUP BY p.prof_id, p.first_name, p.last_name;"
  },
  {
    "question": "What is the average GPA of students who are in their final year of study (year of study = 4) across each major department? Return exactly these columns in order: dept_name, average_gpa.",
    "sql": "SELECT d.dept_name, AVG(s.gpa) AS average_gpa FROM departments d JOIN students s ON d.dept_id = s.major_dept_id WHERE s.year_of_study = 4 GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "Which professors have supervised or taught more than 15 distinct students across all their offerings? Return exactly these columns in order: first_name, last_name, distinct_students.",
    "sql": "SELECT p.first_name, p.last_name, COUNT(DISTINCT e.student_id) AS distinct_students FROM professors p JOIN offerings o ON p.prof_id = o.prof_id JOIN enrollments e ON o.offering_id = e.offering_id GROUP BY p.prof_id, p.first_name, p.last_name HAVING COUNT(DISTINCT e.student_id) > 15;"
  },
  {
    "question": "Find the total number of withdrawals ('W') grade recorded for each department offering courses. Return exactly these columns in order: dept_name, withdrawal_count.",
    "sql": "SELECT d.dept_name, COUNT(e.enrollment_id) AS withdrawal_count FROM departments d JOIN courses c ON d.dept_id = c.dept_id JOIN offerings o ON c.course_id = o.course_id JOIN enrollments e ON o.offering_id = e.offering_id WHERE e.grade = 'W' GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "Find the average salary of professors hired in each decade. Return exactly these columns in order: decade, avg_salary.",
    "sql": "SELECT (CAST(strftime('%Y', hire_date) AS INT) / 10) * 10 AS decade, AVG(salary) AS avg_salary FROM professors WHERE hire_date IS NOT NULL GROUP BY decade;"
  },
  {
    "question": "Show the number of students majoring in each department who have a GPA higher than 3.5. Return exactly these columns in order: dept_name, excellent_students.",
    "sql": "SELECT d.dept_name, COUNT(s.student_id) AS excellent_students FROM departments d JOIN students s ON d.dept_id = s.major_dept_id WHERE s.gpa > 3.5 GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "Find the total number of credits taught in each semester of 2024. Return exactly these columns in order: semester, total_credits.",
    "sql": "SELECT o.semester, SUM(c.credits) AS total_credits FROM offerings o JOIN courses c ON o.course_id = c.course_id WHERE o.year = 2024 GROUP BY o.semester;"
  },
  {
    "question": "Identify departments with budgets greater than 500,000 where the average professor salary is also greater than 80,000. Return exactly these columns in order: dept_name, budget, avg_salary.",
    "sql": "SELECT d.dept_name, d.budget, AVG(p.salary) AS avg_salary FROM departments d JOIN professors p ON d.dept_id = p.dept_id WHERE d.budget > 500000 GROUP BY d.dept_id, d.dept_name, d.budget HAVING AVG(p.salary) > 80000;"
  },
  {
    "question": "What is the maximum GPA of students majoring in each department, showing only major departments with a maximum GPA of at least 3.8? Return exactly these columns in order: dept_name, max_gpa.",
    "sql": "SELECT d.dept_name, MAX(s.gpa) AS max_gpa FROM departments d JOIN students s ON d.dept_id = s.major_dept_id GROUP BY d.dept_id, d.dept_name HAVING MAX(s.gpa) >= 3.8;"
  },
  {
    "question": "Find the total number of students enrolled in each building's course offerings. Return exactly these columns in order: building, enrollment_count.",
    "sql": "SELECT d.building, COUNT(e.enrollment_id) AS enrollment_count FROM departments d JOIN courses c ON d.dept_id = c.dept_id JOIN offerings o ON c.course_id = o.course_id JOIN enrollments e ON o.offering_id = e.offering_id WHERE d.building IS NOT NULL GROUP BY d.building;"
  },
  {
    "question": "How many courses in each department have a max enrollment of 50 or more? Return exactly these columns in order: dept_name, large_course_count.",
    "sql": "SELECT d.dept_name, COUNT(c.course_id) AS large_course_count FROM departments d JOIN courses c ON d.dept_id = c.dept_id WHERE c.max_enrollment >= 50 GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "Show the average salary of professors group by whether they are tenured or not, but only for departments in Smith Hall. Return exactly these columns in order: is_tenured, average_salary.",
    "sql": "SELECT p.is_tenured, AVG(p.salary) AS average_salary FROM professors p JOIN departments d ON p.dept_id = d.dept_id WHERE d.building = 'Smith Hall' GROUP BY p.is_tenured;"
  },
  {
    "question": "Find the total number of students enrolled in offerings taught by professors from their own major department. Return exactly these columns in order: local_enrollments.",
    "sql": "SELECT COUNT(*) AS local_enrollments FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN professors p ON o.prof_id = p.prof_id WHERE s.major_dept_id = p.dept_id;"
  },
  {
    "question": "Calculate the average GPA of students who are graduating in each month/year combination. Return exactly these columns in order: graduation_period, avg_gpa, student_count.",
    "sql": "SELECT strftime('%Y-%m', graduation_date) AS graduation_period, AVG(gpa) AS avg_gpa, COUNT(*) AS student_count FROM students WHERE graduation_date IS NOT NULL GROUP BY graduation_period;"
  },
  {
    "question": "Find the departments that have deans with a salary greater than 140,000. Return exactly these columns in order: dept_name, first_name, last_name, salary.",
    "sql": "SELECT d.dept_name, p.first_name, p.last_name, p.salary FROM departments d JOIN professors p ON d.dean_id = p.prof_id WHERE p.salary > 140000;"
  },
  {
    "question": "Which years had more than 50 course offerings? Return exactly these columns in order: year, offering_count.",
    "sql": "SELECT year, COUNT(offering_id) AS offering_count FROM offerings GROUP BY year HAVING COUNT(offering_id) > 50;"
  },
  {
    "question": "Show the average max enrollment for courses taught in the 'Fall' semester compared to 'Spring' semester. Return exactly these columns in order: semester, average_capacity.",
    "sql": "SELECT o.semester, AVG(c.max_enrollment) AS average_capacity FROM offerings o JOIN courses c ON o.course_id = c.course_id WHERE o.semester IN ('Fall', 'Spring') GROUP BY o.semester;"
  },
  {
    "question": "What is the total budget for all departments combined? Return exactly these columns in order: grand_total_budget.",
    "sql": "SELECT SUM(budget) AS grand_total_budget FROM departments;"
  },
  {
    "question": "Find the list of departments that have at least 1 course with 4 credits and 1 course with 3 credits. Return exactly these columns in order: dept_name.",
    "sql": "SELECT d.dept_name FROM departments d JOIN courses c ON d.dept_id = c.dept_id WHERE c.credits IN (3, 4) GROUP BY d.dept_id, d.dept_name HAVING COUNT(DISTINCT c.credits) = 2;"
  },
  {
    "question": "Find the total, maximum, and minimum credits available across all courses. Return exactly these columns in order: total_credits, max_credits, min_credits.",
    "sql": "SELECT SUM(credits) AS total_credits, MAX(credits) AS max_credits, MIN(credits) AS min_credits FROM courses;"
  },
  {
    "question": "For each major department, calculate the total budget spent on deans. Return exactly these columns in order: dept_name, dean_salary_total.",
    "sql": "SELECT d.dept_name, SUM(p.salary) AS dean_salary_total FROM departments d JOIN professors p ON d.dean_id = p.prof_id GROUP BY d.dept_id, d.dept_name;"
  },
  {
    "question": "Show the average GPA of students in the entire database. Return exactly these columns in order: overall_average_gpa.",
    "sql": "SELECT AVG(gpa) AS overall_average_gpa FROM students;"
  },
  {
    "question": "Find the department with the absolute lowest average professor salary. Return exactly these columns in order: dept_name, average_salary.",
    "sql": "SELECT d.dept_name, AVG(p.salary) AS average_salary FROM departments d JOIN professors p ON d.dept_id = p.dept_id GROUP BY d.dept_id, d.dept_name ORDER BY average_salary ASC LIMIT 1;"
  },
  {
    "question": "Find the names of students who have a GPA higher than the average GPA of students in their own major department. Return exactly these columns in order: first_name, last_name, gpa.",
    "sql": "SELECT s1.first_name, s1.last_name, s1.gpa FROM students s1 WHERE s1.gpa > (SELECT AVG(s2.gpa) FROM students s2 WHERE s2.major_dept_id = s1.major_dept_id);"
  },
  {
    "question": "Identify all professors whose salaries are higher than the dean of their department. Return exactly these columns in order: first_name, last_name, salary, dept_name.",
    "sql": "SELECT p.first_name, p.last_name, p.salary, d.dept_name FROM professors p JOIN departments d ON p.dept_id = d.dept_id WHERE p.salary > (SELECT dean.salary FROM professors dean WHERE dean.prof_id = d.dean_id);"
  },
  {
    "question": "Which students are enrolled in offerings taught by professors earning more than 120,000? Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN professors p ON o.prof_id = p.prof_id WHERE p.salary > 120000;"
  },
  {
    "question": "Find the list of courses that have been offered in 2024 but never in 2023. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT DISTINCT c.course_code, c.title FROM courses c JOIN offerings o ON c.course_id = o.course_id WHERE o.year = 2024 AND c.course_id NOT IN (SELECT DISTINCT course_id FROM offerings WHERE year = 2023);"
  },
  {
    "question": "Find the department dean details for the department with the maximum budget. Return all columns.",
    "sql": "SELECT * FROM professors WHERE prof_id = (SELECT dean_id FROM departments WHERE budget = (SELECT MAX(budget) FROM departments));"
  },
  {
    "question": "List students who have a GPA lower than the average GPA of all students in the university. Return exactly these columns in order: first_name, last_name, gpa.",
    "sql": "SELECT first_name, last_name, gpa FROM students WHERE gpa < (SELECT AVG(gpa) FROM students);"
  },
  {
    "question": "Identify courses with a maximum enrollment limit strictly greater than the average maximum enrollment limit of courses in department ID 3. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE max_enrollment > (SELECT AVG(max_enrollment) FROM courses WHERE dept_id = 3);"
  },
  {
    "question": "Which professors belong to a department located in 'Main Hall'? Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE dept_id IN (SELECT dept_id FROM departments WHERE building = 'Main Hall');"
  },
  {
    "question": "Find the students who got the highest grade 'A' in the course 'CS101' in 2024. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE student_id IN (SELECT student_id FROM enrollments e JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id WHERE e.grade = 'A' AND c.course_code = 'CS101' AND o.year = 2024);"
  },
  {
    "question": "What is the average GPA of students who are not majoring in the 'Computer Science' department? Return exactly these columns in order: average_gpa.",
    "sql": "SELECT AVG(gpa) AS average_gpa FROM students WHERE major_dept_id NOT IN (SELECT dept_id FROM departments WHERE dept_name = 'Computer Science') OR major_dept_id IS NULL;"
  },
  {
    "question": "List professors who earn more than the average salary of tenured professors. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE salary > (SELECT AVG(salary) FROM professors WHERE is_tenured = TRUE);"
  },
  {
    "question": "Find all departments that have a budget higher than the average budget of all departments in the university. Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments WHERE budget > (SELECT AVG(budget) FROM departments);"
  },
  {
    "question": "Which students are enrolled in more than 3 course offerings? Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE student_id IN (SELECT student_id FROM enrollments GROUP BY student_id HAVING COUNT(*) > 3);"
  },
  {
    "question": "Find the offerings taught by the dean of the 'Biology' department. Return all columns.",
    "sql": "SELECT * FROM offerings WHERE prof_id = (SELECT dean_id FROM departments WHERE dept_name = 'Biology');"
  },
  {
    "question": "Which courses have a maximum enrollment that is higher than the average maximum enrollment of all courses offered in 2025? Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE max_enrollment > (SELECT AVG(c.max_enrollment) FROM courses c JOIN offerings o ON c.course_id = o.course_id WHERE o.year = 2025);"
  },
  {
    "question": "Find all students who have enrolled in at least one course taught by Professor 'Alan Turing'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT DISTINCT s.first_name, s.last_name FROM students s JOIN enrollments e ON s.student_id = e.student_id WHERE e.offering_id IN (SELECT offering_id FROM offerings o JOIN professors p ON o.prof_id = p.prof_id WHERE p.first_name = 'Alan' AND p.last_name = 'Turing');"
  },
  {
    "question": "List departments that have no tenured professors. Return exactly these columns in order: dept_name.",
    "sql": "SELECT dept_name FROM departments WHERE dept_id NOT IN (SELECT DISTINCT dept_id FROM professors WHERE is_tenured = TRUE AND dept_id IS NOT NULL);"
  },
  {
    "question": "What is the total number of enrollments for courses offered by the department that has the highest budget? Return exactly these columns in order: total_enrollments.",
    "sql": "SELECT COUNT(*) AS total_enrollments FROM enrollments e JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id WHERE c.dept_id = (SELECT dept_id FROM departments WHERE budget = (SELECT MAX(budget) FROM departments));"
  },
  {
    "question": "Find the student who has enrolled in the maximum number of courses in the Fall of 2024. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE student_id = (SELECT student_id FROM enrollments e JOIN offerings o ON e.offering_id = o.offering_id WHERE o.semester = 'Fall' AND o.year = 2024 GROUP BY student_id ORDER BY COUNT(*) DESC LIMIT 1);"
  },
  {
    "question": "Find courses that have been offered in 'Spring 2024' and have more than 5 enrollments. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE course_id IN (SELECT o.course_id FROM offerings o JOIN enrollments e ON o.offering_id = e.offering_id WHERE o.semester = 'Spring' AND o.year = 2024 GROUP BY o.offering_id, o.course_id HAVING COUNT(e.enrollment_id) > 5);"
  },
  {
    "question": "Show the first name, last name, and GPA of students whose GPA is within the top 3 GPAs in the university. Return exactly these columns in order: first_name, last_name, gpa.",
    "sql": "SELECT first_name, last_name, gpa FROM students WHERE gpa IN (SELECT DISTINCT gpa FROM students ORDER BY gpa DESC LIMIT 3);"
  },
  {
    "question": "Find the departments that do not have any professors earning less than 60,000. Return exactly these columns in order: dept_name.",
    "sql": "SELECT dept_name FROM departments WHERE dept_id NOT IN (SELECT DISTINCT dept_id FROM professors WHERE salary < 60000 AND dept_id IS NOT NULL);"
  },
  {
    "question": "Identify student enrollments where the enrolled course is worth strictly fewer credits than the maximum credits offered by any course in the university. Return exactly these columns in order: enrollment_id, first_name, last_name, title.",
    "sql": "SELECT e.enrollment_id, s.first_name, s.last_name, c.title FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id WHERE c.credits < (SELECT MAX(credits) FROM courses);"
  },
  {
    "question": "What is the average GPA of students who got an 'A' grade in any course? Return exactly these columns in order: average_gpa.",
    "sql": "SELECT AVG(gpa) AS average_gpa FROM students WHERE student_id IN (SELECT DISTINCT student_id FROM enrollments WHERE grade = 'A');"
  },
  {
    "question": "Show details of the oldest hired professor (minimum hire date) in each building. Return exactly these columns in order: p.*, building.",
    "sql": "SELECT p.*, d.building FROM professors p JOIN departments d ON p.dept_id = d.dept_id WHERE p.hire_date = (SELECT MIN(p2.hire_date) FROM professors p2 JOIN departments d2 ON p2.dept_id = d2.dept_id WHERE d2.building = d.building);"
  },
  {
    "question": "List professors who have taught at least one course in 'Fall 2024' but have never taught 'Spring 2024'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE prof_id IN (SELECT DISTINCT prof_id FROM offerings WHERE semester = 'Fall' AND year = 2024) AND prof_id NOT IN (SELECT DISTINCT prof_id FROM offerings WHERE semester = 'Spring' AND year = 2024);"
  },
  {
    "question": "Find courses whose department has a budget that is above the average budget of all departments. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE dept_id IN (SELECT dept_id FROM departments WHERE budget > (SELECT AVG(budget) FROM departments));"
  },
  {
    "question": "Retrieve the first name, last name, and salary of professors who earn more than the average salary of professors in the 'Mathematics' department. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE salary > (SELECT AVG(salary) FROM professors WHERE dept_id = (SELECT dept_id FROM departments WHERE dept_name = 'Mathematics'));"
  },
  {
    "question": "Show the rank of each student based on their GPA within the entire university, using CTE. Return exactly these columns in order: student_id, first_name, last_name, gpa, gpa_rank.",
    "sql": "WITH student_gpa_ranks AS (SELECT student_id, first_name, last_name, gpa, RANK() OVER (ORDER BY gpa DESC) AS gpa_rank FROM students) SELECT first_name, last_name, gpa, gpa_rank FROM student_gpa_ranks;"
  },
  {
    "question": "Identify students who are in the top 2 GPAs in their respective major departments. Return exactly these columns in order: student_id, first_name, last_name, major_dept_id, gpa, pos.",
    "sql": "WITH ranked_students AS (SELECT student_id, first_name, last_name, major_dept_id, gpa, ROW_NUMBER() OVER (PARTITION BY major_dept_id ORDER BY gpa DESC) AS pos FROM students) SELECT rs.first_name, rs.last_name, rs.gpa, d.dept_name FROM ranked_students rs JOIN departments d ON rs.major_dept_id = d.dept_id WHERE rs.pos <= 2;"
  },
  {
    "question": "Show details of all professors along with the running total of salaries inside their respective departments. Return exactly these columns in order: first_name, last_name, dept_name, salary, running_salary_total.",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name, p.salary, SUM(p.salary) OVER (PARTITION BY p.dept_id ORDER BY p.hire_date ASC) AS running_salary_total FROM professors p JOIN departments d ON p.dept_id = d.dept_id;"
  },
  {
    "question": "Find each department name, its budget, and the budget difference compared to the department with the next lowest budget. Return exactly these columns in order: dept_name, budget, prev_budget.",
    "sql": "WITH sorted_depts AS (SELECT dept_name, budget, LAG(budget, 1) OVER (ORDER BY budget ASC) AS prev_budget FROM departments) SELECT dept_name, budget, budget - prev_budget AS budget_diff FROM sorted_depts;"
  },
  {
    "question": "For each student enrollment, calculate the rank of the grade they received within that specific offering (based on GPA equivalents: A=4, A-=3.7, B+=3.3, B=3, B-=2.7, C+=2.3, C=2, D=1, F=0). Return exactly these columns in order: enrollment_id, first_name, last_name, offering_id, grade, grade_rank.",
    "sql": "WITH enrollment_grades AS (SELECT e.enrollment_id, s.first_name, s.last_name, e.offering_id, e.grade, RANK() OVER (PARTITION BY e.offering_id ORDER BY CASE e.grade WHEN 'A' THEN 4.0 WHEN 'A-' THEN 3.7 WHEN 'B+' THEN 3.3 WHEN 'B' THEN 3.0 WHEN 'B-' THEN 2.7 WHEN 'C+' THEN 2.3 WHEN 'C' THEN 2.0 WHEN 'D' THEN 1.0 ELSE 0.0 END DESC) AS grade_rank FROM enrollments e JOIN students s ON e.student_id = s.student_id) SELECT first_name, last_name, offering_id, grade, grade_rank FROM enrollment_grades;"
  },
  {
    "question": "Using a CTE, find all professors who have taught at least 3 offerings in any year, and show their details. Return exactly these columns in order: prof_id, year, taught_count.",
    "sql": "WITH active_profs AS (SELECT prof_id, year, COUNT(*) AS taught_count FROM offerings GROUP BY prof_id, year HAVING COUNT(*) >= 3) SELECT p.first_name, p.last_name, ap.year, ap.taught_count FROM professors p JOIN active_profs ap ON p.prof_id = ap.prof_id;"
  },
  {
    "question": "Find the difference between each professor's salary and the maximum salary in their department. Return exactly these columns in order: first_name, last_name, dept_name, salary, salary_gap.",
    "sql": "SELECT p.first_name, p.last_name, d.dept_name, p.salary, MAX(p.salary) OVER (PARTITION BY p.dept_id) - p.salary AS salary_gap FROM professors p JOIN departments d ON p.dept_id = d.dept_id;"
  },
  {
    "question": "Show the list of students, their major, and the running average GPA in that major. Return exactly these columns in order: first_name, last_name, dept_name, gpa, running_avg_gpa.",
    "sql": "SELECT s.first_name, s.last_name, d.dept_name, s.gpa, AVG(s.gpa) OVER (PARTITION BY s.major_dept_id ORDER BY s.student_id ASC) AS running_avg_gpa FROM students s JOIN departments d ON s.major_dept_id = d.dept_id;"
  },
  {
    "question": "Find the department with the most enrolled students across all its offered courses, showing total enrollments. Return exactly these columns in order: dept_id, total_enrolls.",
    "sql": "WITH dept_enrollments AS (SELECT c.dept_id, COUNT(e.enrollment_id) AS total_enrolls FROM enrollments e JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id GROUP BY c.dept_id) SELECT d.dept_name, de.total_enrolls FROM departments d JOIN dept_enrollments de ON d.dept_id = de.dept_id ORDER BY de.total_enrolls DESC LIMIT 1;"
  },
  {
    "question": "Rank departments based on the total credit hours of courses they offer. Return exactly these columns in order: dept_id, total_credits.",
    "sql": "WITH dept_credits AS (SELECT dept_id, SUM(credits) AS total_credits FROM courses GROUP BY dept_id) SELECT d.dept_name, dc.total_credits, RANK() OVER (ORDER BY dc.total_credits DESC) AS credit_rank FROM departments d JOIN dept_credits dc ON d.dept_id = dc.dept_id;"
  },
  {
    "question": "Get the percentage of deans in the university who earn more than 130,000. Return exactly these columns in order: salary.",
    "sql": "WITH dean_salaries AS (SELECT p.salary FROM departments d JOIN professors p ON d.dean_id = p.prof_id) SELECT (CAST(COUNT(CASE WHEN salary > 130000 THEN 1 END) AS REAL) / COUNT(*)) * 100 AS percentage_high_paid_deans FROM dean_salaries;"
  },
  {
    "question": "Find the cumulative number of students enrolled per date (chronological order). Return exactly these columns in order: enrollment_date, daily_count.",
    "sql": "WITH enrollment_dates AS (SELECT enrollment_date, COUNT(*) AS daily_count FROM enrollments GROUP BY enrollment_date) SELECT enrollment_date, daily_count, SUM(daily_count) OVER (ORDER BY enrollment_date ASC) AS cumulative_enrollments FROM enrollment_dates;"
  },
  {
    "question": "Which students are taking courses taught by their advisor or dean? Show student full name and course title. Return exactly these columns in order: first_name, last_name, title.",
    "sql": "SELECT s.first_name, s.last_name, c.title FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN offerings o ON e.offering_id = o.offering_id JOIN courses c ON o.course_id = c.course_id JOIN departments d ON s.major_dept_id = d.dept_id WHERE o.prof_id = d.dean_id;"
  },
  {
    "question": "Determine the highest-paid professor in each building. Return exactly these columns in order: p.*, building, rn.",
    "sql": "WITH ranked_profs AS (SELECT p.*, d.building, ROW_NUMBER() OVER (PARTITION BY d.building ORDER BY p.salary DESC) AS rn FROM professors p JOIN departments d ON p.dept_id = d.dept_id WHERE d.building IS NOT NULL) SELECT first_name, last_name, building, salary FROM ranked_profs WHERE rn = 1;"
  },
  {
    "question": "Find all courses that had at least 3 offerings in 2024, and rank them by their max enrollment limits. Return exactly these columns in order: course_id, offering_count.",
    "sql": "WITH course_offerings_2024 AS (SELECT course_id, COUNT(*) AS offering_count FROM offerings WHERE year = 2024 GROUP BY course_id HAVING COUNT(*) >= 3) SELECT c.course_code, c.title, c.max_enrollment, RANK() OVER (ORDER BY c.max_enrollment DESC) AS capacity_rank FROM courses c JOIN course_offerings_2024 co ON c.course_id = co.course_id;"
  },
  {
    "question": "For each student, show the semester they took their first class and the semester they took their most recent class. Return exactly these columns in order: student_id, semester, year, first_rn, last_rn.",
    "sql": "WITH chronological_enrollments AS (SELECT e.student_id, o.semester, o.year, ROW_NUMBER() OVER (PARTITION BY e.student_id ORDER BY o.year ASC, CASE o.semester WHEN 'Spring' THEN 1 WHEN 'Summer' THEN 2 WHEN 'Fall' THEN 3 END ASC) AS first_rn, ROW_NUMBER() OVER (PARTITION BY e.student_id ORDER BY o.year DESC, CASE o.semester WHEN 'Spring' THEN 3 WHEN 'Summer' THEN 2 WHEN 'Fall' THEN 1 END DESC) AS last_rn FROM enrollments e JOIN offerings o ON e.offering_id = o.offering_id) SELECT s.first_name, s.last_name, f.semester AS first_sem, f.year AS first_yr, l.semester AS last_sem, l.year AS last_yr FROM students s JOIN chronological_enrollments f ON s.student_id = f.student_id AND f.first_rn = 1 JOIN chronological_enrollments l ON s.student_id = l.student_id AND l.last_rn = 1;"
  },
  {
    "question": "Find the average GPA of students who are majoring in a department whose budget is larger than the total budget of all departments in the same building combined. Return exactly these columns in order: building, total_b.",
    "sql": "WITH building_totals AS (SELECT building, SUM(budget) AS total_b FROM departments WHERE building IS NOT NULL GROUP BY building) SELECT AVG(s.gpa) AS average_gpa FROM students s JOIN departments d ON s.major_dept_id = d.dept_id JOIN building_totals bt ON d.building = bt.building WHERE d.budget > (bt.total_b - d.budget);"
  },
  {
    "question": "Identify students who got an 'A' grade in at least 2 distinct courses, and show their details. Return exactly these columns in order: student_id, a_offerings.",
    "sql": "WITH excellent_students AS (SELECT student_id, COUNT(DISTINCT offering_id) AS a_offerings FROM enrollments WHERE grade = 'A' GROUP BY student_id HAVING COUNT(DISTINCT offering_id) >= 2) SELECT s.first_name, s.last_name, s.gpa FROM students s JOIN excellent_students es ON s.student_id = es.student_id;"
  },
  {
    "question": "Find all students who have a GPA higher than 3.9. Return exactly these columns in order: first_name, last_name, gpa.",
    "sql": "SELECT first_name, last_name, gpa FROM students WHERE gpa > 3.9;"
  },
  {
    "question": "Retrieve the first name, last name, and salary of all professors who are tenured. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE is_tenured = TRUE;"
  },
  {
    "question": "List all departments with budgets strictly below 450,000. Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments WHERE budget < 450000;"
  },
  {
    "question": "List all courses offered with 4 credits. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE credits = 4;"
  },
  {
    "question": "Retrieve all offering details where the semester is 'Spring' and the year is 2025. Return all columns.",
    "sql": "SELECT * FROM offerings WHERE semester = 'Spring' AND year = 2025;"
  },
  {
    "question": "Find all students in their second year of study. Return exactly these columns in order: first_name, last_name, gpa.",
    "sql": "SELECT first_name, last_name, gpa FROM students WHERE year_of_study = 2;"
  },
  {
    "question": "Retrieve the names of professors hired on or before December 31, 2018. Return exactly these columns in order: first_name, last_name, hire_date.",
    "sql": "SELECT first_name, last_name, hire_date FROM professors WHERE hire_date <= '2018-12-31';"
  },
  {
    "question": "List all buildings where university departments are located, removing duplicates. Return exactly these columns in order: building.",
    "sql": "SELECT DISTINCT building FROM departments WHERE building IS NOT NULL;"
  },
  {
    "question": "Find courses that have a maximum enrollment limit between 30 and 60 students. Return exactly these columns in order: course_code, title, max_enrollment.",
    "sql": "SELECT course_code, title, max_enrollment FROM courses WHERE max_enrollment BETWEEN 30 AND 60;"
  },
  {
    "question": "Find all students who have a GPA in the range of 2.8 to 3.2. Return exactly these columns in order: first_name, last_name, gpa.",
    "sql": "SELECT first_name, last_name, gpa FROM students WHERE gpa BETWEEN 2.8 AND 3.2;"
  },
  {
    "question": "Show details of professors whose last name is 'Smith'. Return all columns.",
    "sql": "SELECT * FROM professors WHERE last_name = 'Smith';"
  },
  {
    "question": "List the details of students who are graduating in May 2026. Return exactly these columns in order: student_id, first_name, last_name, graduation_date.",
    "sql": "SELECT student_id, first_name, last_name, graduation_date FROM students WHERE graduation_date BETWEEN '2026-05-01' AND '2026-05-31';"
  },
  {
    "question": "Show the salaries of the top 3 highest-paid professors. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors ORDER BY salary DESC LIMIT 3;"
  },
  {
    "question": "Find all distinct semesters in the offerings table. Return exactly these columns in order: semester.",
    "sql": "SELECT DISTINCT semester FROM offerings;"
  },
  {
    "question": "Retrieve the first 5 students enrolled in the system, ordered by student ID. Return exactly these columns in order: student_id, first_name, last_name.",
    "sql": "SELECT student_id, first_name, last_name FROM students ORDER BY student_id ASC LIMIT 5;"
  },
  {
    "question": "Find all enrollments that received a grade of 'B+' or 'B'. Return all columns.",
    "sql": "SELECT * FROM enrollments WHERE grade IN ('B+', 'B');"
  },
  {
    "question": "Which courses have course codes starting with 'MATH'? Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE course_code LIKE 'MATH%';"
  },
  {
    "question": "Find details of departments that do have a dean assigned. Return all columns.",
    "sql": "SELECT * FROM departments WHERE dean_id IS NOT NULL;"
  },
  {
    "question": "List all professors who are not tenured and earn less than 80,000. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE is_tenured = FALSE AND salary < 80000;"
  },
  {
    "question": "Find all students who have a graduation date specified. Return exactly these columns in order: first_name, last_name, graduation_date.",
    "sql": "SELECT first_name, last_name, graduation_date FROM students WHERE graduation_date IS NOT NULL;"
  },
  {
    "question": "Find enrollments registered on '2024-09-10'. Return all columns.",
    "sql": "SELECT * FROM enrollments WHERE enrollment_date = '2024-09-10';"
  },
  {
    "question": "List the 5 longest-serving professors based on hire date. Return exactly these columns in order: first_name, last_name, hire_date.",
    "sql": "SELECT first_name, last_name, hire_date FROM professors WHERE hire_date IS NOT NULL ORDER BY hire_date ASC LIMIT 5;"
  },
  {
    "question": "Find all courses that are worth 2 or 3 credits. Return exactly these columns in order: course_code, title, credits.",
    "sql": "SELECT course_code, title, credits FROM courses WHERE credits IN (2, 3);"
  },
  {
    "question": "List courses with max enrollment greater than or equal to 80. Return exactly these columns in order: course_code, title, max_enrollment.",
    "sql": "SELECT course_code, title, max_enrollment FROM courses WHERE max_enrollment >= 80;"
  },
  {
    "question": "List all students whose study year is strictly greater than 4. Return exactly these columns in order: first_name, last_name, year_of_study.",
    "sql": "SELECT first_name, last_name, year_of_study FROM students WHERE year_of_study > 4;"
  },
  {
    "question": "Find all distinct buildings where departments are housed. Return exactly these columns in order: building.",
    "sql": "SELECT DISTINCT building FROM departments WHERE building IS NOT NULL;"
  },
  {
    "question": "Get all offerings for the year 2024. Return all columns.",
    "sql": "SELECT * FROM offerings WHERE year = 2024;"
  },
  {
    "question": "Find professors who have a salary strictly above 140,000. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE salary > 140000;"
  },
  {
    "question": "Find students whose last name is 'Davis'. Return exactly these columns in order: student_id, first_name, gpa.",
    "sql": "SELECT student_id, first_name, gpa FROM students WHERE last_name = 'Davis';"
  },
  {
    "question": "Which departments have a budget strictly between 1,000,000 and 3,000,000? Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments WHERE budget BETWEEN 1000000 AND 3000000;"
  },
  {
    "question": "Retrieve offerings taught in the Fall semester. Return exactly these columns in order: offering_id, course_id, prof_id.",
    "sql": "SELECT offering_id, course_id, prof_id FROM offerings WHERE semester = 'Fall';"
  },
  {
    "question": "List courses with titles that contain the word 'Science'. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE title LIKE '%Science%';"
  },
  {
    "question": "Find the last name, GPA, and year of study of students with a GPA strictly above 3.8. Return exactly these columns in order: last_name, gpa, year_of_study.",
    "sql": "SELECT last_name, gpa, year_of_study FROM students WHERE gpa > 3.8;"
  },
  {
    "question": "List all distinct grades given in course enrollments. Return exactly these columns in order: grade.",
    "sql": "SELECT DISTINCT grade FROM enrollments WHERE grade IS NOT NULL;"
  },
  {
    "question": "Find the names of professors hired in 2020. Return exactly these columns in order: first_name, last_name, hire_date.",
    "sql": "SELECT first_name, last_name, hire_date FROM professors WHERE hire_date BETWEEN '2020-01-01' AND '2020-12-31';"
  },
  {
    "question": "Show the list of department names sorted in alphabetical order. Return exactly these columns in order: dept_name.",
    "sql": "SELECT dept_name FROM departments ORDER BY dept_name ASC;"
  },
  {
    "question": "Show offerings of course ID 7. Return exactly these columns in order: offering_id, semester, year.",
    "sql": "SELECT offering_id, semester, year FROM offerings WHERE course_id = 7;"
  },
  {
    "question": "List students who will graduate in the year 2027. Return exactly these columns in order: first_name, last_name, graduation_date.",
    "sql": "SELECT first_name, last_name, graduation_date FROM students WHERE graduation_date BETWEEN '2027-01-01' AND '2027-12-31';"
  },
  {
    "question": "Show details of the department with dean ID equal to 15. Return all columns.",
    "sql": "SELECT * FROM departments WHERE dean_id = 15;"
  },
  {
    "question": "Get courses that are 2 credit hours. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE credits = 2;"
  },
  {
    "question": "List the first names and last names of students with GPA exactly equal to 3.0. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE gpa = 3.0;"
  },
  {
    "question": "Find all enrollments recorded before September 1, 2024. Return all columns.",
    "sql": "SELECT * FROM enrollments WHERE enrollment_date < '2024-09-01';"
  },
  {
    "question": "Find professors who have a salary between 60,000 and 90,000. Return exactly these columns in order: first_name, last_name, salary.",
    "sql": "SELECT first_name, last_name, salary FROM professors WHERE salary BETWEEN 60000 AND 90000;"
  },
  {
    "question": "List the first and last name of students whose year of study is greater than 2, ordered by year of study. Return exactly these columns in order: first_name, last_name, year_of_study.",
    "sql": "SELECT first_name, last_name, year_of_study FROM students WHERE year_of_study > 2 ORDER BY year_of_study ASC;"
  },
  {
    "question": "Show details of courses that have a maximum enrollment of exactly 40. Return all columns.",
    "sql": "SELECT * FROM courses WHERE max_enrollment = 40;"
  },
  {
    "question": "Find all offerings from the Fall semester of 2023. Return exactly these columns in order: offering_id, course_id, prof_id.",
    "sql": "SELECT offering_id, course_id, prof_id FROM offerings WHERE semester = 'Fall' AND year = 2023;"
  },
  {
    "question": "Which departments have a budget of less than 500,000? Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments WHERE budget < 500000;"
  },
  {
    "question": "Find all students whose first name starts with 'M' and ends with 'y'. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE first_name LIKE 'M%y';"
  },
  {
    "question": "List all departments, ordered by their budget descending. Return exactly these columns in order: dept_name, budget.",
    "sql": "SELECT dept_name, budget FROM departments ORDER BY budget DESC;"
  },
  {
    "question": "Retrieve courses belonging to department ID 4. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE dept_id = 4;"
  },
  {
    "question": "Find professors who were hired in September of any year. Return exactly these columns in order: first_name, last_name, hire_date.",
    "sql": "SELECT first_name, last_name, hire_date FROM professors WHERE hire_date LIKE '%-09-%';"
  },
  {
    "question": "List all students whose GPA is less than 3.0 and who are in their second year. Return exactly these columns in order: first_name, last_name, gpa.",
    "sql": "SELECT first_name, last_name, gpa FROM students WHERE gpa < 3.0 AND year_of_study = 2;"
  },
  {
    "question": "Find the course offerings of course ID 8 in the Spring semester. Return exactly these columns in order: offering_id, year.",
    "sql": "SELECT offering_id, year FROM offerings WHERE course_id = 8 AND semester = 'Spring';"
  },
  {
    "question": "Which enrollments have a grade of 'C' or 'D'? Return exactly these columns in order: enrollment_id, student_id, grade.",
    "sql": "SELECT enrollment_id, student_id, grade FROM enrollments WHERE grade IN ('C', 'D');"
  },
  {
    "question": "Get the names of all tenured professors in department 3. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE is_tenured = TRUE AND dept_id = 3;"
  },
  {
    "question": "Show course title and max enrollment for courses with more than 2 credits. Return exactly these columns in order: title, max_enrollment.",
    "sql": "SELECT title, max_enrollment FROM courses WHERE credits > 2;"
  },
  {
    "question": "List all students with last name 'Jones' or first name 'Michael'. Return exactly these columns in order: student_id, first_name, last_name.",
    "sql": "SELECT student_id, first_name, last_name FROM students WHERE last_name = 'Jones' OR first_name = 'Michael';"
  },
  {
    "question": "What is the department ID of the department with name 'Biology'? Return exactly these columns in order: dept_id.",
    "sql": "SELECT dept_id FROM departments WHERE dept_name = 'Biology';"
  },
  {
    "question": "List the details of the top 5 students by GPA in their 3rd year. Return all columns.",
    "sql": "SELECT * FROM students WHERE year_of_study = 3 ORDER BY gpa DESC LIMIT 5;"
  },
  {
    "question": "Which professors have a non-null hire date? Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE hire_date IS NOT NULL;"
  },
  {
    "question": "Find all courses that do not belong to department ID 2. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE dept_id != 2 OR dept_id IS NULL;"
  },
  {
    "question": "List all offerings that are not scheduled for the year 2025. Return all columns.",
    "sql": "SELECT * FROM offerings WHERE year != 2025;"
  },
  {
    "question": "Retrieve student first name and last name where student ID is between 150 and 200. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM students WHERE student_id BETWEEN 150 AND 200;"
  },
  {
    "question": "Find the building name for the department named 'History'.",
    "sql": "SELECT building FROM departments WHERE dept_name = 'History';"
  },
  {
    "question": "Select courses with credit values of 3 or 4. Return exactly these columns in order: course_code, title.",
    "sql": "SELECT course_code, title FROM courses WHERE credits IN (3, 4);"
  },
  {
    "question": "List all students whose graduation date is set after the year 2027. Return exactly these columns in order: first_name, last_name, graduation_date.",
    "sql": "SELECT first_name, last_name, graduation_date FROM students WHERE graduation_date > '2027-12-31';"
  },
  {
    "question": "Find all enrollments with enrollment date equal to '2024-09-01'. Return all columns.",
    "sql": "SELECT * FROM enrollments WHERE enrollment_date = '2024-09-01';"
  },
  {
    "question": "Retrieve details of department number 3. Return all columns.",
    "sql": "SELECT * FROM departments WHERE dept_id = 3;"
  },
  {
    "question": "Find professors who have a salary of exactly 90,000. Return exactly these columns in order: first_name, last_name.",
    "sql": "SELECT first_name, last_name FROM professors WHERE salary = 90000;"
  }
]
