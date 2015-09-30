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
DEFAULT_ADVANTURE_NAME = 'new_advanture'

API_URL = 'http://dicebota-api.appspot.com/'