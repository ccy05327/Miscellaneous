# Different Versions of Grade

## Version 1

### Read file

20220204

`grade.ipynb`

    Read `output.json` copied from inspector -> network -> GetDegreeHomeCalendar

## Version 2

### Scrape and use `selenium` to login

20220210

`grade.py`

    Download Chrome Driver.

    Fill in `chrome_drive_path`, `email`, and `password` with seleium webdriver on Coursera login, redirect to degree homepage, press `left_button` _twice_ to get to Jan 24th's week, grab the target's xPath(s) and fill it in, print out the outcome.

## Version 3

### Use `selenium`'s chrome driver manager

20220211

`grade_1.py`

    Download Chrome Driver.

    Fill in `chrome_drive_path`, `binary_path` (chrome.exe), `user_data_dir`, `profile_dir`.

    To get the above paths, use `selenium` to open chrome and open a new tab, type `chrome://version`, make sure profile_dir is not random text.

    First time user has to create a new Profile/User without logging in when prompt the opened Chrome (do not login with your own accoutn), and login to your Coursera account. The profile will remember your login details.

## Version 4

### Use Notion API to gather results

20220211~

`notion_api.ipynb`, `notion.json` (scraped)

--- [Template Used](https://prettystatic.com/notion-api-python/) ---

    Read database (existing database)

    Create Page (within the database)

    Update Page (within the database)

#### **TODO**

1. Update the page with

   {
   "Grade": {
   "type": "number",
   "number": `things_in_content`
   },
   "Date": {
   "type": "date",
   "date": {
   "start": `current_time`
   }
   },
   "Module": {
   "type": "title",
   "title": [
   "type": "text",
   "text: {
   "content": `title`
   }
   ]
   }
   }

2. Require `page_id` to update on the same page with the same module (later no need to update `Module`)

3. If the `Grade` is not `Number` (i.e. "In Review"), try and except empty value.
