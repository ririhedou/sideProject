"""
editted by ketian
to save the screenshot of the page
"""

from automation import TaskManager, CommandSequence
import datetime
import os
import filtering
import filtering_subdomain
import time


import sys
reload(sys)
sys.setdefaultencoding('utf8')

BROWSER_DATA = '/mnt/sdb1/browser_data/'


def my_custom_get_final_url(site, record, **kwargs):
    driver = kwargs['driver']
    print ('[CUSTOM]INDEX RECORD'),
    print (record.idx)
    record.print_record()
    record.set_final_url(driver.current_url)
    print ('[CUSTOM]REDIRECTION CHAIN')
    record.print_url_chain()
    print(driver.current_url.decode('utf-8'))


def run_open_wpm(records, outputdir=None):

    # The list of sites that we wish to crawl
    NUM_BROWSERS = 1

    # Loads the manager preference and 3 copies of the default browser dictionaries
    manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

    # Update browser configuration (use this for per-browser settings)
    for i in xrange(NUM_BROWSERS):
        browser_params[i]['http_instrument'] = True # Record HTTP Requests and Responses
        browser_params[i]['disable_flash'] = False #Enable flash for all three browsers
        browser_params[i]['headless'] = True  #Launch every browser headless

    # Update TaskManager configuration (use this for crawl-wide settings)
    if not outputdir:
        browser_data = BROWSER_DATA
    else:
        browser_data = outputdir

    manager_params['data_directory'] = browser_data
    manager_params['log_directory'] = browser_data

    # Instantiates the measurement platform
    # Commands time out by default after 60 seconds
    manager = TaskManager.TaskManager(manager_params, browser_params)

    # Visits the sites with all browsers simultaneously
    # cur_time = datetime.datetime.now().strftime("(%I_%M%p_on_%B_%d_%Y)")
    day = datetime.datetime.now().strftime("[%B_%d_%Y]")

    c = 0

    for record in records:

        site = record.url
        name = record.idx

        screen_name = name + '[k]' + day + '.screen'
        page_source = name + '[k]' + day + '.source'

        print ("screen name", screen_name)
        print ("page_source name", page_source)

        #screen_name = domain_tld_full_name + cur_time +'.screen'
        #page_source = domain_tld_full_name + cur_time +'.source'

        TIMEOUT = 30

        try:
            command_sequence = CommandSequence.CommandSequence(site)

            # Start by visiting the page
            command_sequence.get(sleep=0, timeout=TIMEOUT)

            command_sequence.run_custom_function(my_custom_get_final_url, (site,record))
            # save screenshot
            command_sequence.save_screenshot(screen_name, timeout=TIMEOUT)
            command_sequence.dump_page_source(page_source, timeout=TIMEOUT)

            # dump_profile_cookies/dump_flash_cookies closes the current tab.
            #command_sequence.dump_profile_cookies(120)
            #command_sequence.dump_profile(dump_folder=DUMP_FOLDER, close_webdriver=False, compress=False, timeout=TIMEOUT)
            #command_sequence.dump_flash_cookies(timeout=TIMEOUT)

            manager.execute_command_sequence(command_sequence, index='**')

        except:

            print ("FUCK the world at {}".format(c))

        c += 1

    # Shuts down the browsers and waits for the data to finish logging
    manager.close()

    print ("Close the manager and done")


def create_local_dir(dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
        print ("we create the dist path as " + dst)

    print ("Done the createment")


def read_files(fname):
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content


if __name__ == "__main__":
    path = './domain_collect/'
    #path = './subdomain_collect/'

    _id = sys.argv[1]
    print (_id)

    if path == './domain_collect/':
        records = filtering.get_redirect_all_from_file_id(path, _id)
    else:
        records = filtering_subdomain.get_redirect_all_from_file_id(path, _id)

    if records is None:
        print ("Too many records, we ignore this")
        sys.exit(1)

    files = os.listdir(path)
    files.sort()
    _id_domain = path + files[int(_id)]

    if path == './domain_collect/':
        _id_domain = _id_domain.split("_")[-1][:-4].replace(".", "_")
    else:
        _id_domain = _id_domain.split("/")[-1][:-4].replace(".", "_")

    _id_domain_folder =_id_domain + "-" + _id

    browser_data = BROWSER_DATA + _id_domain_folder

    create_local_dir(browser_data)

    n = len(records)
    if n > 500:
        print ("we split the records")
        for i in range(0, n, 500):
            cur_records = records[i:i+500]
            run_open_wpm(cur_records, outputdir=browser_data)
            time.sleep(20)
    else:
        run_open_wpm(records, outputdir=browser_data)
    #move_file_to_local_dir(browser_data, _id)