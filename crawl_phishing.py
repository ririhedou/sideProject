from automation import TaskManager, CommandSequence
"""
editted by ketian
to save the screenshot of the page
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def run_open_wpm_for_records(records):
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
    #TODO you have to modify here
    browser_data = '/media/fbeyond/APPs/Phishing/browser_data/'

    manager_params['data_directory'] = browser_data
    manager_params['log_directory'] = browser_data

    # Instantiates the measurement platform
    # Commands time out by default after 60 seconds
    manager = TaskManager.TaskManager(manager_params, browser_params)

    c = 0
    for r in records:

        screen_name = str(r.idx) + '.screen'
        page_source = str(r.idx) + '.source'
        site = r.url

        print ("screen name", screen_name)
        print ("page_source name", page_source)

        #screen_name = domain_tld_full_name + cur_time +'.screen'
        #page_source = domain_tld_full_name + cur_time +'.source'

        TIMEOUT = 10

        command_sequence = CommandSequence.CommandSequence(site)

        # Start by visiting the page
        command_sequence.get(sleep=0, timeout=TIMEOUT)

        # save screenshot
        command_sequence.save_screenshot(screen_name, timeout=TIMEOUT)
        command_sequence.dump_page_source(page_source, timeout=TIMEOUT)

        # dump_profile_cookies/dump_flash_cookies closes the current tab.
        #command_sequence.dump_profile_cookies(120)
        #command_sequence.dump_profile(dump_folder=DUMP_FOLDER, close_webdriver=False, compress=False, timeout=TIMEOUT)
        #command_sequence.dump_flash_cookies(timeout=TIMEOUT)

        manager.execute_command_sequence(command_sequence, index='**')
        c += 1
    # Shuts down the browsers and waits for the data to finish logging
    manager.close()

    print ("Done the crawler")
    #move_file_to_local_dir(screen_path, source_path, screens, sources, folder)

if __name__ == "__main__":
    _id = sys.argv[1]
    print (_id)