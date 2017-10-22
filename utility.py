import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from functools import wraps
from os import environ
from pdb import set_trace
from time import sleep
import sys, os
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from collections import deque

TIME_BEFORE_QUIT = 4
FAILURES_BEFORE_QUIT = 4

def flog(fname, level = 'info'):

    """Logs a message

    Args:
        message (str): the message to be logged.
        level (str):  debug level
    """


    def f(message):

        logging.basicConfig(filename=fname,level=logging.DEBUG,format='%(asctime)s %(message)s' )
        {"info": logging.info, "debug" : logging.debug, "warning" : logging.warning}[level](message)

    return f

def log(message, level = 'info'):

    """Logs a message

    Args:
        message (str): the message to be logged.
        level (str):  debug level
    """

    print (message)
    logging.basicConfig(filename='history.log',level=logging.DEBUG,format='%(asctime)s %(message)s' )
    {"info": logging.info, "debug" : logging.debug, "warning" : logging.warning}[level](message)

def extract_user_name_and_password(level):
    as_upper = level.upper()
    keys = {
            "username": f'CIVIS_{as_upper}_USERNAME',
            "password": f'CIVIS_{as_upper}_PASSWORD'
            }

    return environ[keys['username']], environ[keys['password']]

def _login(level='local'):

    driver = webdriver.Chrome()
    log ("Beginning to login")
    login_url = "http://platform.civis.dev:3000/users/sign_in"
    driver.get(login_url)

    user_name, password = extract_user_name_and_password(level)

    u_input = driver.find_element_by_xpath('//*[@id="user_login"]')
    p_input = driver.find_element_by_xpath('//*[@id="user_password"]')

    u_input.clear()
    p_input.clear()

    u_input.send_keys(user_name)
    p_input.send_keys(password)
    res = driver.find_element_by_xpath('//*[@id="new_user"]/div[3]/input').click()

    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "welcome_index")))
    except Exception as e:
        driver.quit()

    return driver


def login(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        driver = _login()
        args_prime = list(args)
        args_prime.insert(0, driver)
        try:
            res = func(*args_prime, **kwargs)
        except Exception as e:
            print ("Exception occured: {}".format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        sleep(TIME_BEFORE_QUIT)
        driver.quit()
    return with_logging


class Queue():

    def __init__(self):
        self.q = deque()

    def enqueue(self, val):
        self.queue.append(val)
        return val

    def get(self):
        return self.queue.popleft()

class Item():

    _id = 0

    def __init__(self, f, name):
        self.f = f
        self.name = name
        self.id = _id
        Item._id +=1

class Action():

    def __init__(self, driver, d):
        self.driver = driver
        self.d = d
        self.queue = deque()

    def enqueue(self, val):
        self.queue.append(val)
        return val

    def run_one(self):
        action = self.queue.popleft()
        action()

    def go(self, trace = False):
        if trace:
            set_trace()
        while len(self.queue):
            self.run_one()

    def find(self, x, ret = True):
        def f():
            xpath = self.d[x]
            def _find(driver, x, i):
                if i == FAILURES_BEFORE_QUIT:
                    raise Exception("Too many times")
                try:
                    return driver.find_element_by_xpath(x)
                except NoSuchElementException:
                    print ("Try again {}".format(i))
                    sleep(2)
                    return _find(driver, x, i + 1)
            return _find(self.driver,xpath, 0)

        if ret:
            return f()
        else:
            return self.enqueue(f)

    def send(self, x, val):
        def f():
            element = self.find(x)
            element.clear()
            element.send_keys(val)
            print ("Sent {} to {}".format(val, x))
        return self.enqueue(f)

    def click(self, xpath):

        def f():
            sleep(1)
            element = self.find(xpath)
            element = WebDriverWait(self.driver, 10).until(
                     EC.element_to_be_clickable((By.XPATH, self.d[xpath])));
            element.click()
            print ("Just clicked {}".format(xpath))
        return self.enqueue(f)

    def zzz(self, time = 1):
        def f():
            print ("Sleeping for {}".format(time))
            return sleep(time)
        return self.enqueue(f)

    def set_code_mirror(self, xpath, value):
        def f():
            el = self.find(xpath)
            self.driver.execute_script("arguments[0].CodeMirror.setValue(\"" + value + "\");", el)
            print ("Set code mirror to {}".format(value))
        return self.enqueue(f)
