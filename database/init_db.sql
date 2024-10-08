-- database/init_db.sql
CREATE DATABASE IF NOT EXISTS survey_suite_db;
USE survey_suite_db;

CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(15),
    EmailAddress VARCHAR(100) UNIQUE NOT NULL,
    RoleID INT
);

CREATE TABLE Role (
    RoleID INT AUTO_INCREMENT PRIMARY KEY,
    RoleName VARCHAR(50) NOT NULL
);

CREATE TABLE Permission (
    PermissionID INT AUTO_INCREMENT PRIMARY KEY,
    PermissionName VARCHAR(50) NOT NULL,
    Description TEXT
);

CREATE TABLE Dashboard (
    DashboardID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Widget JSON,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE Response (
    response_id INT AUTO_INCREMENT PRIMARY KEY,
    survey_id INT NOT NULL,
    respondent_id INT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_response_survey FOREIGN KEY (survey_id) REFERENCES Survey(survey_id) ON DELETE CASCADE,
    CONSTRAINT fk_respondent FOREIGN KEY (respondent_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Survey (
    survey_id INT AUTO_INCREMENT PRIMARY KEY,
    creator_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_creator FOREIGN KEY (creator_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Question (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    survey_id INT NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    CONSTRAINT fk_survey FOREIGN KEY (survey_id) REFERENCES Survey(survey_id) ON DELETE CASCADE
);

CREATE TABLE QuestionOption (
    option_id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_text VARCHAR(255) NOT NULL,
    CONSTRAINT fk_question FOREIGN KEY (question_id) REFERENCES Question(question_id) ON DELETE CASCADE
);



CREATE TABLE Template (
    TemplateID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    Content TEXT,
    CreatedBy INT,
    FOREIGN KEY (CreatedBy) REFERENCES User(UserID)
);

CREATE TABLE Report (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    SurveyID INT NOT NULL,
    GeneratedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Content TEXT,
    FOREIGN KEY (SurveyID) REFERENCES Survey(SurveyID)
);

CREATE TABLE API (
    APIID INT AUTO_INCREMENT PRIMARY KEY,
    Endpoint VARCHAR(255) NOT NULL,
    Description TEXT,
    Method ENUM('GET', 'POST', 'PUT', 'DELETE') NOT NULL
);

CREATE TABLE Answer (
    answer_id INT AUTO_INCREMENT PRIMARY KEY,
    response_id INT NOT NULL,
    question_id INT NOT NULL,
    answer_text TEXT NOT NULL, -- Can store either text or selected option IDs
    CONSTRAINT fk_answer_response FOREIGN KEY (response_id) REFERENCES Response(response_id) ON DELETE CASCADE,
    CONSTRAINT fk_answer_question FOREIGN KEY (question_id) REFERENCES Question(question_id) ON DELETE CASCADE
);