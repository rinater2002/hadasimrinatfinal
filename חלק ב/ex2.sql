DROP TABLE IF EXISTS FamilyTree;
DROP TABLE IF EXISTS Persons;

-- Create the main table
CREATE TABLE Persons (
    Person_Id INT PRIMARY KEY,
    Personal_Name VARCHAR(50),
    Family_Name VARCHAR(50),
    Gender ENUM('זכר', 'נקבה'),
    Father_Id INT,
    Mother_Id INT,
    Spouse_Id INT
);

-- Insert data
INSERT INTO Persons (Person_Id, Personal_Name, Family_Name, Gender, Father_Id, Mother_Id, Spouse_Id) VALUES
(1, 'Aharon',   'Poper', 'זכר', NULL, NULL, 2),
(2, 'Lea',   'Poper', 'נקבה', NULL, NULL, 1),
(3, 'Avigail',  'Poper', 'נקבה', 1, 2, NULL),
(4, 'Motty',   'Poper', 'זכר', 1, 2, NULL),
(5, 'Dan',  'Oren',  'זכר', NULL, NULL, 3),
(6, 'Tal',    'Oren',  'נקבה', 5, 3, NULL),
(7, 'Itamar',   'Swimmer', 'זכר', NULL, NULL, 8),
(8, 'Rinat',  'Ehrenfreund' , 'נקבה', NULL, NULL, NULL);


-- Create the FamilyTree table
CREATE TABLE FamilyTree (
    Person_Id INT,
    Relative_Id INT,
    Connection_Type VARCHAR(20),
    PRIMARY KEY (Person_Id, Relative_Id, Connection_Type)
);


-- Add Father relationships (אב)
INSERT INTO FamilyTree (Person_Id, Relative_Id, Connection_Type)
SELECT Person_Id, Father_Id, 'אב'
FROM Persons
WHERE Father_Id IS NOT NULL;

-- Add Mother relationships (אם)
INSERT INTO FamilyTree (Person_Id, Relative_Id, Connection_Type)
SELECT Person_Id, Mother_Id, 'אם'
FROM Persons
WHERE Mother_Id IS NOT NULL;

-- Add Spouse relationships (בן זוג / בת זוג)
-- For males: 'בת זוג', for females: 'בן זוג'
INSERT INTO FamilyTree (Person_Id, Relative_Id, Connection_Type)
SELECT 
    p1.Person_Id,
    p1.Spouse_Id,
    CASE 
        WHEN p1.Gender = 'זכר' THEN 'בת זוג'
        WHEN p1.Gender = 'נקבה' THEN 'בן זוג'
    END AS Connection_Type
FROM Persons p1
WHERE p1.Spouse_Id IS NOT NULL;

-- Add Children (בן / בת)
INSERT INTO FamilyTree (Person_Id, Relative_Id, Connection_Type)
SELECT 
    p.Parent_Id,
    p.Person_Id,
    CASE 
        WHEN child.Gender = 'זכר' THEN 'בן'
        WHEN child.Gender = 'נקבה' THEN 'בת'
    END AS Connection_Type
FROM (
    SELECT Person_Id, Father_Id AS Parent_Id FROM Persons WHERE Father_Id IS NOT NULL
    UNION ALL
    SELECT Person_Id, Mother_Id AS Parent_Id FROM Persons WHERE Mother_Id IS NOT NULL
) p
JOIN Persons child ON p.Person_Id = child.Person_Id;


-- Add Sibling relationships (אח / אחות)
INSERT INTO FamilyTree (Person_Id, Relative_Id, Connection_Type)
SELECT 
    p1.Person_Id,
    p2.Person_Id,
    CASE 
        WHEN p2.Gender = 'זכר' THEN 'אח'
        WHEN p2.Gender = 'נקבה' THEN 'אחות'
    END AS Connection_Type
FROM Persons p1
JOIN Persons p2 ON (
    p1.Person_Id <> p2.Person_Id AND (
        (p1.Father_Id IS NOT NULL AND p1.Father_Id = p2.Father_Id) OR
        (p1.Mother_Id IS NOT NULL AND p1.Mother_Id = p2.Mother_Id)
    )
);
-- Complete missing spouse connections in Persons table
UPDATE Persons p1
JOIN Persons p2 ON p1.Spouse_Id = p2.Person_Id
SET p2.Spouse_Id = p1.Person_Id
WHERE p1.Spouse_Id IS NOT NULL
  AND (p2.Spouse_Id IS NULL OR p2.Spouse_Id <> p1.Person_Id);

-- Insert missing spouse connections into FamilyTree table
INSERT INTO FamilyTree (Person_Id, Relative_Id, Connection_Type)
SELECT 
    p1.Person_Id,
    p1.Spouse_Id,
    CASE 
        WHEN p1.Gender = 'זכר' THEN 'בת זוג'
        WHEN p1.Gender = 'נקבה' THEN 'בן זוג'
    END AS Connection_Type
FROM Persons p1
WHERE p1.Spouse_Id IS NOT NULL
  AND NOT EXISTS (
      SELECT 1
      FROM FamilyTree ft
      WHERE ft.Person_Id = p1.Person_Id
        AND ft.Relative_Id = p1.Spouse_Id
        AND (ft.Connection_Type = 'בן זוג' OR ft.Connection_Type = 'בת זוג')
  );


-- Final family tree
SELECT * FROM FamilyTree ORDER BY Person_Id, Connection_Type;
