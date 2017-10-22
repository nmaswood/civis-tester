from utility import login, log, Action
import sys
from time import sleep
from functools import wraps
from pdb import set_trace

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@login
def civp_8880(driver):
    d = {
            'scripts_menu_button': '/html/body/civis-side-menu/div[1]/div/div[3]/a[3]',
            'new_script_button': '/html/body/div[4]/div/div[4]/civis-resize-wrapper/div/ng-transclude/civis-resize-right/div/ng-transclude/div/div/ui-view/div/fco-index-container/div/div/div[1]/button',
            'new_sql_script': '/html/body/civis-side-pane/div/div/div/scripts-add-pane/div/div[2]/div[1]/a',
            'code_mirror_input': '/html/body/div[4]/div/div[4]/civis-resize-wrapper/div/ng-transclude/civis-resize-right/div/ng-transclude/div/div/ui-view/div/div/scripts-detail/div/fco-details-container/div/div/div/div[3]/div[5]/div[1]',
            'notify_button': "/html/body/div[4]/div/div[4]/civis-resize-wrapper/div/ng-transclude/civis-resize-right/div/ng-transclude/div/div/ui-view/div/div/scripts-detail/div/fco-details-container/div/div/div/div[1]/div[2]/div/fco-actions/span[3]",
            'subject_input': "/html/body/civis-side-pane/div/div/div/div/div[1]/notifier/div/div/div[1]/div[3]/div[4]/input",
            'email_input': "/html/body/civis-side-pane/div/div/div/div/div[1]/notifier/div/div/div[1]/div[3]/div[6]/textarea",
            'close_button': "/html/body/civis-side-pane/div/button",
            'run_button': "/html/body/div[4]/div/div[4]/civis-resize-wrapper/div/ng-transclude/civis-resize-right/div/ng-transclude/div/div/ui-view/div/div/scripts-detail/div/fco-details-container/div/div/div/div[3]/div[2]/div/div[1]/fco-special-actions/div/div/span[5]/span/button"
            }

    browse = Action(driver, d)
    browse.click('scripts_menu_button')
    browse.click('scripts_menu_button')
    browse.zzz(4)
    browse.click('new_script_button')
    browse.click('new_sql_script')
    browse.set_code_mirror('code_mirror_input', "SELECT 1;")
    browse.click('notify_button')
    browse.zzz(4)
    browse.send('subject_input', "Test 1: SELECT 1;")
    browse.send('email_input', "Look at this [report]{{file_url}}")
    browse.click('close_button')
    browse.click('run_button')
    browse.go()

    """
    click(driver, d['scripts_menu_button'])
    click(driver, d['new_script_button'])
    click(driver, d['new_sql_script'])
    set_code_mirror(driver, d['code_mirror_input'], "SELECT 1;")
    click(driver, d['notify_button'])
    set_trace()
    send(driver, d['subject_input'], "Test 1: SELECT 1;")
    send(driver, d['email_input'], "Look at this [report]{{file_url}}")
    click(driver, d['close_button'])
    click(driver, d['run_button'])
    """

for _ in range(1):
    civp_8880()
