DROP TABLE IF EXISTS user; --if db already exists 
DROP TABLE IF EXISTS jobPost;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    
    password TEXT NOT NULL
);

CREATE TABLE jobPost (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    poster_id INTEGER NOT NULL,
    applydate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, --date applied to the job
    jobtitle TEXT NOT NULL, --name/title of opening
    jobURL TEXT NOT NULL, --url for job posting
    --location !!figure out a good way to store city/state/?nation
    --desc  -desc of job title, might be too long to include
    --resume, cov-letter, etc...
    --status -pending, rejected, accepted, interview, etc...ABORT
    
    FOREIGN KEY (poster_id) REFERENCES user (id)
);