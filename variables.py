# file store all variables and setting information.


MAIN_PAGE_HTML = """\
    <form action='/roll?%s' method='post'>
        <div><textarea name='content' row='3' clos='60'></textarea></div>
        <div><input type='submit' value='roll dice'></div>
    </form>
    <form>Switch Advanture:
        <input value='%s' name="advanture_name">
        <input type="submit" value='switch'>
    </form>
    <a href='%s'>%s</a>
"""
DEFAULT_ADVANTURE_NAME = 'RE_FETCH_DICE_ROLLnew_advanture'

API_URL = 'http://dicebota-api.appspot.com/'

RE_FETCH_DICE_ROLL = r' *(\d{1,2})[dD](\d{1,3}) *([+-])* *(\d{1,3})* *([kK]\d{1})* *([\u4e00-\u9fa5A-Za-z0-9][\u4e00-\u9fa5A-Za-z0-9 ]*)*'
