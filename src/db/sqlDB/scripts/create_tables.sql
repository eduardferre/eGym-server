USE TestDB
GO

IF NOT EXISTS (SELECT *
FROM sysobjects
WHERE name='users' and xtype='U')
    CREATE TABLE dbo.users
(
    id UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWID(),
    username VARCHAR(255) NOT NULL UNIQUE,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    birthDate DATE NOT NULL
)
GO

IF NOT EXISTS (SELECT *
FROM sysobjects
WHERE name='exercises' and xtype='U')
    CREATE TABLE dbo.exercises
(
    id UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWID(),
    creator VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL UNIQUE,
    description VARCHAR(255)
)
GO

IF NOT EXISTS (SELECT *
FROM sysobjects
WHERE name='routines' and xtype='U')
    CREATE TABLE dbo.routines
(
    id UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWID(),
    creator VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255)
)
GO

IF NOT EXISTS (SELECT *
FROM sysobjects
WHERE name='relationRoutinesExercises' and xtype='U')
    CREATE TABLE dbo.relationRoutinesExercises
(
    routineId UNIQUEIDENTIFIER,
    exerciseId UNIQUEIDENTIFIER,

    FOREIGN KEY (routineId) REFERENCES dbo.routines(id),
    FOREIGN KEY (exerciseId) REFERENCES dbo.exercises(id),
    UNIQUE (routineId, exerciseId)
)
GO