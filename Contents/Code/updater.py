UPDATED_AT = 'updater.updated_at'

class GithubStrategy(object):
    def __init__(self, repo, branch = 'master'):
        super(GithubStrategy, self).__init__()
        self.repo        = repo
        self.branch      = branch
        self.archive_url = 'https://github.com/%s/archive/%s.zip'  % (repo, branch)
        self.atom_url    = 'https://github.com/%s/commits/%s.atom' % (repo, branch)

    @property
    def updated_at(self):
        feed    = RSS.FeedFromURL(self.atom_url)
        updated = Datetime.ParseDate(feed.entries[0].updated)

        return updated.replace(tzinfo = None)

instance = None
def init(**kwargs):
    global instance
    instance = strategy(**kwargs)

def updated_at():
    if UPDATED_AT in Dict:
        return Dict[UPDATED_AT]
    else:
        return None

def update_available():
    last_updated = updated_at()
    if last_updated is None:
        return True
    else:
        return last_updated < instance.updated_at

def PerformUpdate():
    if update_available():
        instance.perform_update()

def add_button_to(container, **kwargs):
    if update_available():
        container.add(DirectoryObject(
            title = L('updater.update'),
            key   = Callback(PerformUpdate)
        ))
