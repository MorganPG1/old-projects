import LoginGen
range = LoginGen.YearRange(2010,2999)
email, password = LoginGen.login.generateEmailAndPassword(range)
print(email,password)