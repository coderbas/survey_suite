-- database/init_db.sql
CREATE DATABASE IF NOT EXISTS survey_suite_db;
USE survey_suite_db;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    finance_no VARCHAR(20) NOT NULL,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    mobile_no VARCHAR(20) NOT NULL,
    email_id VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    section VARCHAR(100)
);

CREATE TABLE Role (
    RoleID INT AUTO_INCREMENT PRIMARY KEY,
    RoleName VARCHAR(50) NOT NULL
);

CREATE TABLE Survey (
    survey_id INT AUTO_INCREMENT PRIMARY KEY,
    creator_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_creator FOREIGN KEY (creator_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE Question (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    survey_id INT NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    CONSTRAINT fk_survey FOREIGN KEY (survey_id) REFERENCES Survey(survey_id) ON DELETE CASCADE
);

CREATE TABLE QuestionOption (
    option_id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_text VARCHAR(255) NOT NULL,
    CONSTRAINT fk_question FOREIGN KEY (question_id) REFERENCES Question(question_id) ON DELETE CASCADE
);

CREATE TABLE Response (
    response_id INT AUTO_INCREMENT PRIMARY KEY,
    survey_id INT NOT NULL,
    respondent_id INT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_response_survey FOREIGN KEY (survey_id) REFERENCES Survey(survey_id) ON DELETE CASCADE,
    CONSTRAINT fk_respondent FOREIGN KEY (respondent_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE Answer (
    answer_id INT AUTO_INCREMENT PRIMARY KEY,
    response_id INT NOT NULL,
    question_id INT NOT NULL,
    answer_text TEXT NOT NULL,
    CONSTRAINT fk_answer_response FOREIGN KEY (response_id) REFERENCES Response(response_id) ON DELETE CASCADE,
    CONSTRAINT fk_answer_question FOREIGN KEY (question_id) REFERENCES Question(question_id) ON DELETE CASCADE
);

-- Additional tables such as Role, API, etc., are left unchanged.


CREATE TABLE Permission (
    PermissionID INT AUTO_INCREMENT PRIMARY KEY,
    PermissionName VARCHAR(50) NOT NULL,
    Description TEXT
);

CREATE TABLE IF NOT EXISTS Dashboard (
    DashboardID INT AUTO_INCREMENT PRIMARY KEY,
    id INT NOT NULL, -- Referencing id from Users table
    Widget JSON, -- Can store JSON widget data
    FOREIGN KEY (id) REFERENCES Users(id) ON DELETE CASCADE
);


CREATE TABLE Template (
    TemplateID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    Content TEXT,
    CreatedBy INT,
    FOREIGN KEY (CreatedBy) REFERENCES Users(id)
);

