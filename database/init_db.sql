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

CREATE TABLE Survey (
    SurveyID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status ENUM('Active', 'Inactive', 'Draft') NOT NULL,
    CreatedBy INT,
    FOREIGN KEY (CreatedBy) REFERENCES User(UserID)
);

CREATE TABLE Question (
    QuestionID INT AUTO_INCREMENT PRIMARY KEY,
    SurveyID INT NOT NULL,
    QuestionType ENUM('Text', 'Multiple Choice', 'Checkbox', 'Dropdown', 'Rating') NOT NULL,
    QuestionText TEXT NOT NULL,
    Options JSON,
    FOREIGN KEY (SurveyID) REFERENCES Survey(SurveyID)
);

CREATE TABLE Response (
    ResponseID INT AUTO_INCREMENT PRIMARY KEY,
    SurveyID INT NOT NULL,
    UserID INT,
    Answer JSON,
    SubmissionDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (SurveyID) REFERENCES Survey(SurveyID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
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
