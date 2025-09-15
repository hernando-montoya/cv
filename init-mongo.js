// MongoDB initialization script
// This script runs when MongoDB container starts for the first time

db = db.getSiblingDB('cv_database');

// Create application user with read/write permissions
db.createUser({
  user: 'cv_app',
  pwd: 'cv_app_password',
  roles: [
    {
      role: 'readWrite',
      db: 'cv_database'
    }
  ]
});

// Create indexes for better performance
db.content.createIndex({ "updated_at": -1 });
db.content.createIndex({ "personalInfo.email": 1 });

print('Database initialization completed successfully');