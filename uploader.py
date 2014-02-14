#uses firefox to login with turnin user/pass. Then for each student looks in the given directory for a csusername/a#.txt and if it finds it it uploads it. If it doesn't, it outputs to console that it couldn't find it.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

turninuser = "";
turninpass = ""
assgn = "02"; #assignment number, used for a1.txt
dirlocation = os.getcwd(); #directory that holds csuserid/a1.txt for students
#to skip past half the alphabet, use line 32.


driver = webdriver.Firefox()
driver.get("https://turnin.microlab.cs.utexas.edu/turnin/webturnin.dll/home");

# Log in:
driver.find_element_by_name("username").send_keys(turninuser);
pw = driver.find_element_by_name("password");
pw.send_keys(turninpass);
pw.send_keys(Keys.RETURN);

#change class
driver.find_element_by_xpath("//select/option[@value='CS313E-53580.GRADER']").click();
driver.find_element_by_name("class").send_keys(Keys.RETURN);
driver.find_element_by_xpath("//input[@value='change class']").click();

#get all students
print(driver.find_elements_by_tag_name("select"))
student = driver.find_element_by_name("user");
students = []
for option in student.find_elements_by_tag_name('option'):
 # if(option.text[0] >= 'N'):
    students.append(option.get_attribute('value'));

#go through students
for s in students:
  try:
    driver.find_element_by_xpath("//select/option[@value='"+ s +"']").click();
    driver.find_element_by_xpath("//input[@value='change user']").click();
  except:
    print 'error on ' + s
    continue
  name = dirlocation + '/' + s + '/assignment_'+ assgn +'.txt'; 
  try:
      with open(name):
        print 'Found files for ' + s;  
        pass
  except IOError:
      print '\tI cant find files for ' + s; 
      continue
  driver.find_element_by_xpath("//input[@type='file']").send_keys(name);
  driver.find_element_by_xpath("//input[@value='Upload']").click();

