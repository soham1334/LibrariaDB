print("few_shots.py loaded")


few_shots = [
    { "Question" :"How many users are in the LibraryUser table",
      "SQLQuery": "SELECT COUNT(*) FROM LibraryUser",
      "SQLResult":"Result of SQL Query",
      "Answer":"7" },
    {
      "Question": "What is the total amount of unpaid fines",
      "SQLQuery": "SELECT SUM(Amount) FROM Fine WHERE PaymentStatus = 'NOT PAID'",
     "SQLResult":"Result of SQL Query",
     "Answer": "300.00" },
    { "Question": "Which users have not paid their fines",
     "SQLQuery": "SELECT DISTINCT CONCAT(U.FirstName, ' ', U.LastName) FROM LibraryUser U JOIN Fine F ON U.UserID = F.UserID WHERE F.PaymentStatus = 'NOT PAID'",
     "SQLResult":"Result of SQL Query",
     "Answer": "Billy Bully" },
    {  "Question": "List the titles of books authored by Haruki Murakami",
  "SQLQuery": "SELECT B.Title FROM Book B JOIN Writes W ON B.BookID = W.BookID JOIN Author A ON W.AuthorID = A.AuthorID WHERE A.FirstName = 'Haruki' AND A.LastName = 'Murakami'",
  "SQLResult":"Result of SQL Query",
  "Answer": ["Kafka på stranden", "1Q84"] },
    { "Question": "How many books are published by 'Klim'",
  "SQLQuery": "SELECT COUNT(*) FROM Book B JOIN Publisher P ON B.PublisherID = P.PublisherID WHERE P.PublisherName = 'Klim'",
  "SQLResult":"Result of SQL Query",
  "Answer": 2 },
    {"Question": "Which user has the highest total unpaid fine",
  "SQLQuery": "SELECT CONCAT(U.FirstName, ' ', U.LastName) FROM LibraryUser U JOIN Fine F ON U.UserID = F.UserID WHERE F.PaymentStatus = 'NOT PAID' GROUP BY U.UserID ORDER BY SUM(F.Amount) DESC LIMIT 1",
  "SQLResult":"Result of SQL Query",
  "Answer": "Billy Bully"},
  {  "Question": "Which book has the highest page count",
  "SQLQuery": "SELECT Title FROM Book WHERE PageCount = (SELECT MAX(PageCount) FROM Book)",
  "SQLResult":"Result of SQL Query",
  "Answer": "Database System Concepts, Sixth Edition" },
    
  { "Question": "List users who currently have a book on loan and have not yet returned it",
  "SQLQuery": "SELECT DISTINCT CONCAT(U.FirstName, ' ', U.LastName) FROM LibraryUser U JOIN Loans L ON U.UserID = L.UserID WHERE L.LoanedStatus = 'LOANED' AND L.ReturnedDate IS NULL",
   "SQLResult":"Result of SQL Query",
  "Answer": ["Sule Altintas", "Fahad Sajad", "Sebastian Sbirna", "Kåre Jørgensen"] },  
  { "Question": "What are the titles of books that have been both loaned and reserved",
  "SQLQuery": "SELECT DISTINCT B.Title FROM Book B JOIN Loans L ON B.BookID = L.BookID JOIN Reserves R ON B.BookID = R.BookID",
  "SQLResult":"Result of SQL Query",
  "Answer": "Windows 8.1 - Effektiv uden touch"  }
  

]
  


             
    


      

    