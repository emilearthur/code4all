import requests

class MyBugzilla:
    def __init__(self, account:str, server:str='https://bugzilla.mozilla.org') -> None:
        self.account = account
        self.server = server
        self.session = requests.Session()

    def bug_link(self, bug_id:int):
        return f'{self.server}/show_bug.cgi?id={str(bug_id)}'

    def get_new_bugs(self):
        call = self.server + '/rest/bug'
        params = {'assigned_to:': self.account,
                  'status': 'NEW',
                  'limit': 10}
        try:
            res = self.session.get(call, params=params).json()
        except requests.exceptions.ConnectionError:
            res = {'bugs': []}

        def _add_link(bug):
            bug['link'] = self.bug_link(bug['id'])
            return bug

        for bug in res['bugs']:
            yield _add_link(bug)