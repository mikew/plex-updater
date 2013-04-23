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

    def perform_update(self):
        archive = Archive.ZipFromURL(self.archive_url)

        for name in archive.Names():
            data    = archive[name]
            parts   = name.split('/')[1:]
            shifted = '/'.join(parts)
            full    = Core.storage.join_path(Core.bundle_path, shifted)

            if '/.' in name: continue

            if full.endswith('/'):
                Core.storage.ensure_dirs(full)
            else:
                Core.storage.save(full, data)

        del archive

strategy = GithubStrategy
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

@route('%s/_update' % PLUGIN_PREFIX)
def PerformUpdate():
    @spawn
    def inner(): update_if_available()
    return ObjectContainer(header = 'Updating', message = 'Please wait while updates are being applied.')

def update_if_available():
    if update_available():
        instance.perform_update()

def add_button_to(container, **kwargs):
    if update_available():
        container.add(DirectoryObject(
            title = L('updater.update'),
            key   = Callback(PerformUpdate)
        ))
