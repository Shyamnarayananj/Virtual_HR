-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 20, 2024 at 02:45 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `virtual_hr`
--

-- --------------------------------------------------------

--
-- Table structure for table `vh_admin`
--

CREATE TABLE `vh_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `email` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_admin`
--

INSERT INTO `vh_admin` (`username`, `password`, `email`) VALUES
('admin', 'admin', 'bgeduscanner@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `vh_apti_question`
--

CREATE TABLE `vh_apti_question` (
  `id` int(11) NOT NULL,
  `question` text NOT NULL,
  `option1` varchar(100) NOT NULL,
  `option2` varchar(100) NOT NULL,
  `option3` varchar(100) NOT NULL,
  `option4` varchar(100) NOT NULL,
  `answer` int(11) NOT NULL,
  `entryby` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_apti_question`
--

INSERT INTO `vh_apti_question` (`id`, `question`, `option1`, `option2`, `option3`, `option4`, `answer`, `entryby`) VALUES
(1, 'In the first 10 overs of a cricket game, the run rate was only 3.2. What should be the run rate in the remaining 40 overs to reach the target of 282 runs?', '6.25', '6.5', '6.75', '7', 1, ''),
(2, 'A grocer has a sale of Rs. 6435, Rs. 6927, Rs. 6855, Rs. 7230 and Rs. 6562 for 5 consecutive months. How much sale must he have in the sixth month so that he gets an average sale of Rs. 6500?', '4991', '5991', '6001', '6991', 1, ''),
(3, 'The average of 20 numbers is zero. Of them, at the most, how many may be greater than zero?', '0', '1', '10', '19', 4, ''),
(4, 'The average weight of 8 person''s increases by 2.5 kg when a new person comes in place of one of them weighing 65 kg. What might be the weight of the new person?', '76 kg', '76.5 kg', '85 kg', 'Data Inadequate', 3, ''),
(5, 'Which one of the following is not a prime number?', '31', '61', '71', '91', 4, ''),
(6, 'What least number must be added to 1056, so that the sum is completely divisible by 23 ?', '2', '3', '18', '21', 1, ''),
(7, '1397 x 1397 = ?', '1951609', '1981709', '18362619', '2031719', 1, ''),
(8, '(935421 x 625) = ?', '575648125', '584638125', '584649125', '585628125', 2, ''),
(9, 'The largest 4 digit number exactly divisible by 88 is:', '9944', '9768', '9988', '8888', 1, ''),
(10, 'Which of the following is a prime number ?', '33', '81', '93', '97', 4, ''),
(11, 'The sum of first five prime numbers is:', '11', '18', '26', '28', 4, ''),
(12, 'The difference of two numbers is 1365. On dividing the larger number by the smaller, we get 6 as quotient and the 15 as remainder. What is the smaller number ?', '240', '270', '295', '360', 2, ''),
(13, 'The smallest 3 digit prime number is:', '101', '103', '109', '113', 1, ''),
(14, 'The sum of first 45 natural numbers is:', '1035', '1280', '2070', '2140', 1, ''),
(15, 'If the number 481 * 673 is completely divisible by 9, then the smallest whole number in place of * will be:', '2', '5', '6', '7', 4, ''),
(16, 'cxv', 'xcv', 'xc', 'df', 'v', 1, 'admin'),
(17, 'cxv', 'xcv', 'xc', 'df', 'v', 1, 'admin'),
(18, 'cxv', 'xcv', 'xc', 'df', 'v', 1, 'admin'),
(19, 'cxv', 'xcv', 'xc', 'df', 'v', 1, 'admin'),
(20, 'cxv', 'xcv', 'xc', 'df', 'v', 1, 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `vh_candidate`
--

CREATE TABLE `vh_candidate` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `dob` varchar(15) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `postal_code` varchar(20) NOT NULL,
  `sslc_school` varchar(50) NOT NULL,
  `sslc_mark` double NOT NULL,
  `hsc_school` varchar(30) NOT NULL,
  `hsc_mark` double NOT NULL,
  `father_name` varchar(20) NOT NULL,
  `father_occupation` varchar(30) NOT NULL,
  `father_jobtype` varchar(20) NOT NULL,
  `father_job_location` varchar(30) NOT NULL,
  `father_annual_income` double NOT NULL,
  `mother_name` varchar(20) NOT NULL,
  `mother_occupation` varchar(30) NOT NULL,
  `mother_jobtype` varchar(20) NOT NULL,
  `mother_job_location` varchar(30) NOT NULL,
  `mother_annual_income` double NOT NULL,
  `resume` varchar(50) NOT NULL,
  `photo` varchar(50) NOT NULL,
  `register_date` varchar(20) NOT NULL,
  `question` varchar(200) NOT NULL,
  `program` varchar(20) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_candidate`
--

INSERT INTO `vh_candidate` (`id`, `name`, `gender`, `dob`, `mobile`, `email`, `username`, `password`, `address`, `city`, `postal_code`, `sslc_school`, `sslc_mark`, `hsc_school`, `hsc_mark`, `father_name`, `father_occupation`, `father_jobtype`, `father_job_location`, `father_annual_income`, `mother_name`, `mother_occupation`, `mother_jobtype`, `mother_job_location`, `mother_annual_income`, `resume`, `photo`, `register_date`, `question`, `program`, `status`) VALUES
(1, 'Harish', 'Male', '10.12.1994', 9685748567, 'bgeduscanner@gmail.com', 'harish', '123456', '45,SG Nagar', 'Salem', '635421', 'BS', 91, 'BS', 92, 'Raj', 'Tailor', '', 'Salem', 200000, 'Vijaya', '', '', '', 0, 'R1resume_001.docx', '', '30-12-2023', '13,17,14,5,4', '15', 0),
(2, 'Praveen', 'Male', '17.08.1999', 8897456795, 'bgeduscanner@gmail.com', 'praveen', '123456', '85, FT Nagar', 'Trichy', '620581', 'TBS', 78, 'TBS', 76, 'Dass', 'Civil Engineer', 'Private', 'Trichy', 300000, 'Radha', 'Teacher', 'Government', 'Trichy', 200000, 'R2resume_0021.docx', '', '01-01-2024', '10,1,4,6,14', '5', 0),
(3, 'Rahul', 'Male', '12.01.1999', 8956726718, 'bgeduscanner@gmail.com', 'rahul', '123456', '45,DDFF', 'Trichy', '625458', 'FF', 81, 'FF', 82, 'Somu', 'Farmer', '', 'RR Puram', 200000, 'Lakshmi', '-', '', '-', 0, 'R3resume_002.docx', 'P3', '18-01-2024', '5,11,3,7,20', '11', 0),
(4, 'Saran', 'Male', '14.02.1999', 8527418526, 'bgeduscanner@gmail.com', 'saran', '123456', '34,DD', 'Tanjore', '623487', 'SS', 90, 'SS', 91, 'Ram', 'Farmer', 'Private', 'Tanjore', 200000, 'Sara', 'house wife', '', '-', 0, 'R4resume_004.docx', '', '19-02-2024', '', '', 0);

-- --------------------------------------------------------

--
-- Table structure for table `vh_experience`
--

CREATE TABLE `vh_experience` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `designation` varchar(30) NOT NULL,
  `experience` varchar(200) NOT NULL,
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `company_name` varchar(50) NOT NULL,
  `location` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_experience`
--

INSERT INTO `vh_experience` (`id`, `username`, `designation`, `experience`, `year`, `month`, `company_name`, `location`) VALUES
(1, 'harish', 'Software Engineer', 'Python developer', 1, 0, 'SSS', 'Chennai'),
(2, 'praveen', 'Developer', 'Python developer', 2, 0, 'Wipro', 'Chennai'),
(3, 'saran', 'Junior Programmer', 'programming', 0, 3, 'SSS', 'Chennai');

-- --------------------------------------------------------

--
-- Table structure for table `vh_interview_question`
--

CREATE TABLE `vh_interview_question` (
  `id` int(11) NOT NULL,
  `question` varchar(200) NOT NULL,
  `answer` varchar(200) NOT NULL,
  `hr_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_interview_question`
--

INSERT INTO `vh_interview_question` (`id`, `question`, `answer`, `hr_id`) VALUES
(1, 'Tell me about yourself?', '', ''),
(2, 'Why do you want to work for our company?', '', ''),
(3, 'What are your greatest strengths and weaknesses?', '', ''),
(4, 'Why are you looking for a change?', '', ''),
(5, 'How would you rate yourself on a scale of 1 to 10?', '', ''),
(6, 'What is your biggest achievement so far?', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `vh_job_provider_register`
--

CREATE TABLE `vh_job_provider_register` (
  `id` int(11) NOT NULL,
  `hr_name` varchar(20) NOT NULL,
  `company_name` varchar(50) NOT NULL,
  `services` varchar(100) NOT NULL,
  `location` varchar(50) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `hr_id` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `approved_status` int(11) NOT NULL,
  `register_date` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_job_provider_register`
--

INSERT INTO `vh_job_provider_register` (`id`, `hr_name`, `company_name`, `services`, `location`, `mobile`, `email`, `hr_id`, `password`, `approved_status`, `register_date`) VALUES
(1, 'Subash', 'RRM', 'Software Development', 'Chennai', 8927536814, 'subashrrm@gmail.com', 'RR025', '123456', 1, '30-01-2024'),
(2, 'Raj', 'Wipro', 'Software', 'Chennai', 9894442716, 'bgeduscanner@gmail.com', 'W1', '1234', 0, '09-02-2024');

-- --------------------------------------------------------

--
-- Table structure for table `vh_joined`
--

CREATE TABLE `vh_joined` (
  `id` int(11) NOT NULL,
  `vid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `hr_id` varchar(20) NOT NULL,
  `candidate` varchar(20) NOT NULL,
  `job_position` varchar(30) NOT NULL,
  `training` varchar(10) NOT NULL,
  `train_days` int(11) NOT NULL,
  `join_date` varchar(20) NOT NULL,
  `start_time` varchar(20) NOT NULL,
  `end_time` varchar(20) NOT NULL,
  `salary` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_joined`
--

INSERT INTO `vh_joined` (`id`, `vid`, `pid`, `hr_id`, `candidate`, `job_position`, `training`, `train_days`, `join_date`, `start_time`, `end_time`, `salary`) VALUES
(1, 1, 3, 'RR025', 'harish', 'Python Developer', 'Yes', 30, '2024-02-01', '9AM', '8PM', 25000);

-- --------------------------------------------------------

--
-- Table structure for table `vh_profile_matched`
--

CREATE TABLE `vh_profile_matched` (
  `id` int(11) NOT NULL,
  `vacancy_id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `interview_status` int(11) NOT NULL,
  `interview_date` varchar(20) NOT NULL,
  `interview_time` varchar(20) NOT NULL,
  `minutes` int(11) NOT NULL,
  `apti` varchar(20) NOT NULL,
  `correct` int(11) NOT NULL,
  `apti_score` double NOT NULL,
  `program_score` double NOT NULL,
  `test_score` double NOT NULL,
  `emotion` varchar(100) NOT NULL,
  `dress_code` varchar(50) NOT NULL,
  `hr_id` varchar(20) NOT NULL,
  `company` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_profile_matched`
--

INSERT INTO `vh_profile_matched` (`id`, `vacancy_id`, `username`, `interview_status`, `interview_date`, `interview_time`, `minutes`, `apti`, `correct`, `apti_score`, `program_score`, `test_score`, `emotion`, `dress_code`, `hr_id`, `company`) VALUES
(3, 1, 'harish', 1, '15-02-2024', '12:05', 30, '3', 0, 0, 0, 0, '', '', 'RR025', 'RRM'),
(4, 2, 'praveen', 4, '20-02-2024', '12:15', 30, '5', 5, 100, 60, 10, 'Surprise', '', 'RR025', 'RRM'),
(5, 2, 'rahul', 1, '15-02-2024', '11:23', 30, '', 0, 0, 0, 0, '', '', 'RR025', 'RRM'),
(6, 2, 'harish', 1, '20-02-2024', '11:23', 30, '', 0, 0, 0, 0, '', '', 'RR025', 'RRM');

-- --------------------------------------------------------

--
-- Table structure for table `vh_program`
--

CREATE TABLE `vh_program` (
  `id` int(11) NOT NULL,
  `language` varchar(20) NOT NULL,
  `program` varchar(200) NOT NULL,
  `min_lines` int(11) NOT NULL,
  `max_lines` int(11) NOT NULL,
  `keywords` varchar(100) NOT NULL,
  `result` varchar(100) NOT NULL,
  `hr_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_program`
--

INSERT INTO `vh_program` (`id`, `language`, `program`, `min_lines`, `max_lines`, `keywords`, `result`, `hr_id`) VALUES
(1, 'C Program', 'C Program to Multiply Two Numbers, I/P=50,2', 8, 15, 'stdio.h,main,printf,scanf', 'q1.txt', ''),
(2, 'CPP', 'Find Largest 3 Numbers Using if Statement, I/P=25,100,85', 14, 20, 'iostream,if,cout', 'q2.txt', ''),
(3, 'C Program', 'C Program to Compute Quotient and Remainder, I/P=100/5', 10, 15, 'stdio.h,main,printf', 'q3.txt', ''),
(4, 'C Program', 'Swap Numbers Using Temporary Variable, I/P=10,20', 10, 15, 'stdio.h,main,printf', 'q4.txt', ''),
(5, 'C Program', 'Program to Check Even or Odd, I/P=30', 10, 15, 'stdio.h,main,printf', 'q5.txt', ''),
(6, 'C Program', 'Sum of Natural Numbers Using for Loop, I/P=5', 10, 15, 'stdio.h,main,printf', 'q6.txt', ''),
(7, 'CPP', 'Check if a number is even or odd. I/P=29', 10, 15, 'iostream,if,cout', 'q7.txt', ''),
(8, 'CPP', 'Write a program to swap two numbers. I/P=50,80', 10, 15, 'iostream,main,cout', 'q8.txt', ''),
(9, 'CPP', 'C++ Program to Calculate Sum of Natural Numbers using for loop, I/P=6', 10, 15, 'iostream,main,cout,for', 'q9.txt', ''),
(10, 'CPP', 'C++ Program to Reverse an Integer using while loop, I/P=246', 12, 20, 'iostream,main,cout,while', 'q10.txt', ''),
(11, 'C Program', 'Multiplication Table Up to 10 using for loop, I/P=8', 10, 15, 'stdio.h,main,printf,for', 'q11.txt', ''),
(12, 'C Program', 'Store Numbers and Calculate Average Using Arrays,I/P: n=3, 12,50,34', 15, 25, 'stdio.h,main,printf', 'q12.txt', ''),
(13, 'C Program', 'Store n no. for student Information in Structure and Display it, I/P: n=2, Raj,2231,94, Vijay,2232,86', 20, 30, 'stdio.h,main,printf,struct', 'q13.txt', ''),
(14, 'C Program', 'C Program to find largest element of an Array, I/P: n=4 # 45,87,93,31', 15, 25, 'stdio.h,main,printf', 'q14.txt', ''),
(15, 'C Program', 'Let see the c program to print half triangle by numbers 1 to 5 using for loop', 15, 25, 'stdio.h,main,printf,for', 'q15.txt', ''),
(16, 'CPP', 'C++ Program to Make a Simple Calculator to Add, Subtract, Multiply or Divide Using switch...case, I/P: * , 100,5', 20, 30, 'iostream,main,cout,swith,case,break', 'q16.txt', ''),
(17, 'CPP', 'C++ Program to Calculate Sum and Average of Numbers Using Arrays, I/P: n=3 # 20,45,25', 20, 30, 'iostream,main,cout', 'q17.txt', ''),
(18, 'CPP', 'Store n no. for Employee Information in Structure and Display it, I/P: n=2 # Nirmal,EM2201,15000, Vani,EM2202,18000', 20, 35, 'iostream,main,cout,struct', 'q18.txt', ''),
(19, 'CPP', 'program to add two numbers using a function, I/P: 48, 32', 10, 15, 'iostream,main,cout', 'q19.txt', ''),
(20, 'CPP', 'CPP Program to calculate Area, Volume using Objects-and-class, I/O: Length=15, Breadth=10, Height=12', 15, 30, 'iostream,main,cout,class,public', 'q20.txt', ''),
(21, 'Java', 'Palindrome program in java. In this java program, we will get a number variable and check whether number is palindrome or not. I/P: 454', 15, 20, 'class,main,int,System', 'q21.txt', ''),
(22, 'Java', 'fibonacci series program in java without using recursion. I/P: 10', 12, 20, 'class,main,int,System', 'q22.txt', ''),
(23, 'Java', 'Prime number program in java. In this java program, we will take a number variable and check whether the number is prime or not. I/P:3', 15, 20, 'class,main,int,System', 'q23.txt', ''),
(24, 'Java', 'factorial Program using for loop in java. I/P: 5', 8, 15, 'class,main,int,System', 'q24.txt', ''),
(25, 'Java', 'create the logic for the RightTrianglePattern *', 10, 20, 'class,main,int,System', 'q25.txt', ''),
(26, 'Java', 'Find the ASCII value of a character through a Java program. I/P: a,g', 10, 15, 'class,main,int,System', 'q26.txt', ''),
(27, 'Java', 'Program to read two integer and print product of them, I/P: 15,10', 5, 15, 'class,main,int,System', 'q27.txt', ''),
(28, 'Java', 'Program to check whether the input year is leap or not, I/P: 2022', 15, 25, 'class,main,int,System', 'q28.txt', ''),
(29, 'Java', 'Program to check Vowel or Consonant using Switch Case, I/P: e', 20, 35, 'class,main,int,System', 'q29.txt', ''),
(30, 'Java', 'Java Program to Check if two Arrays are Equal or not, I/P: 30,25,40 # 30,25,40', 10, 20, 'class,main,int,System', 'q30.txt', ''),
(31, 'PHP', 'Factorial of given number, I/P: 5', 20, 35, '?php,form,POST,input', 'q31.txt', ''),
(32, 'PHP', 'Calculate Given 2 numbers by Selected Operator using switch case, I/P: - , 45,20', 20, 40, '?php,form,POST,input,switch,case', 'q32.txt', ''),
(33, 'PHP', 'Biggest of given 3 numbers using if condition, I/P: 58,148,137', 20, 40, '?php,form,POST,input,if', 'q33.txt', ''),
(34, 'PHP', 'Find given number is odd or even using function, I/P: 250', 25, 35, '?php,form,POST,input,function', 'q34.txt', ''),
(35, 'PHP', 'Sum of n Numbers using array, I/P: 150,80,30,40', 15, 25, '?php,array', 'q35.txt', '');

-- --------------------------------------------------------

--
-- Table structure for table `vh_qualification`
--

CREATE TABLE `vh_qualification` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `level` varchar(20) NOT NULL,
  `qualification` varchar(30) NOT NULL,
  `passout_year` varchar(20) NOT NULL,
  `percentage` double NOT NULL,
  `college` varchar(50) NOT NULL,
  `arrears` int(11) NOT NULL,
  `cleared` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_qualification`
--

INSERT INTO `vh_qualification` (`id`, `username`, `level`, `qualification`, `passout_year`, `percentage`, `college`, `arrears`, `cleared`) VALUES
(1, 'harish', 'UG-Engineering', 'BE CSE', '2018', 85, 'SSA', 0, 0),
(2, 'praveen', 'UG-Engineering', 'BE ECE', '2020', 76, 'SCE', 2, 2),
(3, 'rahul', 'UG-Engineering', 'BE ECE', '2021', 80, 'SS', 1, 1),
(4, 'saran', 'PG-Arts', 'MCA', '2020', 85, 'BB', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `vh_temp`
--

CREATE TABLE `vh_temp` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `pid` int(11) NOT NULL,
  `qid` int(11) NOT NULL,
  `uans` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_temp`
--

INSERT INTO `vh_temp` (`id`, `username`, `pid`, `qid`, `uans`) VALUES
(1, 'praveen', 4, 10, 1),
(2, 'praveen', 4, 1, 1),
(3, 'praveen', 4, 4, 1),
(4, 'praveen', 4, 6, 1),
(5, 'praveen', 4, 14, 1);

-- --------------------------------------------------------

--
-- Table structure for table `vh_temp2`
--

CREATE TABLE `vh_temp2` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `pid` int(11) NOT NULL,
  `qid` int(11) NOT NULL,
  `uans` text NOT NULL,
  `answer_st` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_temp2`
--

INSERT INTO `vh_temp2` (`id`, `username`, `pid`, `qid`, `uans`, `answer_st`) VALUES
(1, 'harish', 4, 1, '', 0),
(2, 'harish', 4, 2, 'For my career development.', 0),
(3, 'harish', 4, 3, '', 0),
(4, 'harish', 4, 4, '', 0),
(5, 'harish', 4, 5, '', 0);

-- --------------------------------------------------------

--
-- Table structure for table `vh_vacancy`
--

CREATE TABLE `vh_vacancy` (
  `id` int(11) NOT NULL,
  `job_title` varchar(50) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `mark_10th` double NOT NULL,
  `mark_12th` double NOT NULL,
  `level` varchar(20) NOT NULL,
  `qualification` varchar(30) NOT NULL,
  `mark_degree` double NOT NULL,
  `arrears` int(11) NOT NULL,
  `sports` varchar(100) NOT NULL,
  `extra_curricular` varchar(100) NOT NULL,
  `skills` varchar(100) NOT NULL,
  `annual_income` double NOT NULL,
  `create_date` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `inw_start_date` varchar(20) NOT NULL,
  `inw_end_date` varchar(20) NOT NULL,
  `start_time` varchar(20) NOT NULL,
  `total_hours` int(11) NOT NULL,
  `num_apti` int(11) NOT NULL,
  `program` varchar(20) NOT NULL,
  `hr_id` varchar(20) NOT NULL,
  `company` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vh_vacancy`
--

INSERT INTO `vh_vacancy` (`id`, `job_title`, `gender`, `mark_10th`, `mark_12th`, `level`, `qualification`, `mark_degree`, `arrears`, `sports`, `extra_curricular`, `skills`, `annual_income`, `create_date`, `inw_start_date`, `inw_end_date`, `start_time`, `total_hours`, `num_apti`, `program`, `hr_id`, `company`) VALUES
(1, 'Python Developer', 'Any', 75, 75, 'UG-Engineering', 'All', 75, 2, '', '', 'Python, Flask, MySQL, Artificial Intelligence', 0, '2024-01-30 20:28:00', '', '', '', 0, 0, '', 'RR025', 'RRM'),
(2, 'Python Developer', 'Any', 60, 60, 'Any', 'Any', 60, 3, '-', '-', 'Python,MySQL,Flask', 0, '2024-02-15 12:07:33', '15-02-2024', '15-02-2024', '11', 6, 5, 'C Program', 'RR025', 'RRM');
