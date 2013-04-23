import plex_nose

class TestUpdater(plex_nose.TestCase):
    def test_updated_at():
        import mock
        @mock.patch.dict(updater.Dict, {updater.UPDATED_AT: None})
        def test():
            eq_(updater.updated_at(), None)

        test()

    def test_updated_at_when_updated():
        import mock
        import datetime

        _updated = datetime.datetime(2013, 1, 1)
        @mock.patch.dict(updater.Dict, {updater.UPDATED_AT: _updated})
        def test():
            eq_(updater.updated_at(), _updated)

        test()

class TestIntegrationStrategy():
    def __init__(self, foo):
        self.foo = foo

    @property
    def updated_at(self):
        import datetime
        now = datetime.datetime.now()
        return now + datetime.timedelta(days = 1)

    def perform_update(self):
        self.performed = True

class TestIntegration(plex_nose.TestCase):
    @classmethod
    def setup_class(cls):
        plex_nose.core.sandbox.publish_api(TestIntegrationStrategy)
        plex_nose.core.sandbox.execute("""
updater.strategy = TestIntegrationStrategy
updater.init(foo = "bar")
""")

    def test_init_calls_strategy():
        eq_(updater.instance.foo, 'bar')

    def test_add_button_to():
        container = ObjectContainer()
        updater.add_button_to(container)
        subject = container.objects[0]

        eq_(len(container), 1)
        eqL_(subject.title, 'updater.label.update-now')
        eqcb_(subject.key, updater.PerformUpdate)

    def test_add_button_to_when_no_update():
        import mock

        @mock.patch.object(updater, 'update_available', return_value = False)
        def test(*a):
            container = ObjectContainer()
            updater.add_button_to(container)
            return container
        container = test()

        eq_(len(container), 0)

    def test_PerformUpdate_returns_dialog():
        container = updater.PerformUpdate()
        eqL_(container.header, 'updater.label.updating')
        eqL_(container.message, 'updater.response.updating')

    def test_update_if_available():
        updater.update_if_available()
        saved_ago = (Datetime.Now() - updater.updated_at()).seconds
        ok_(updater.instance.performed)
        ok_(saved_ago < 1)

#GithubUpdateStrategy
#can update code
class TestGithubStrategy(plex_nose.TestCase):
    @classmethod
    def setup_class(cls):
        plex_nose.publish_local_file('Contents/Tests/github-archive.zip',
                name = 'example_archive')

        plex_nose.publish_local_file('Contents/Tests/github-atom.xml',
                name = 'atom_feed')

    def test_can_init():
        subject = updater.GithubStrategy('owner/repo')

        eq_(subject.archive_url,
                'https://github.com/owner/repo/archive/master.zip')
        eq_(subject.atom_url,
                'https://github.com/owner/repo/commits/master.atom')

    def test_can_init_with_branch():
        subject = updater.GithubStrategy('owner/repo', branch = 'stable')

        eq_(subject.archive_url,
                'https://github.com/owner/repo/archive/stable.zip')
        eq_(subject.atom_url,
                'https://github.com/owner/repo/commits/stable.atom')

    def test_updated_at():
        import mock
        import datetime

        feed = RSS.FeedFromString(atom_feed)

        @mock.patch.object(RSS, 'FeedFromURL', return_value = feed)
        def test(*a):
            subject = updater.GithubStrategy('owner/repo')
            actual = subject.updated_at
            expected = datetime.datetime(2013, 4, 14,
                    12, 28, 1, 0, actual.tzinfo)

            eq_(actual, expected)
        test()

    def test_perform_update_extracts_code():
        import mock

        # example_archive structure:
        # channel.bundle/
        # channel.bundle/.hidden
        # channel.bundle/.hidden-dir/
        # channel.bundle/.hidden-dir/file
        # channel.bundle/dir/
        # channel.bundle/dir/file
        # channel.bundle/file

        @mock.patch.object(Archive, 'ZipFromURL', return_value = Archive.Zip(example_archive))
        @mock.patch.object(Core.storage, 'ensure_dirs')
        @mock.patch.object(Core.storage, 'save')
        def test(file_mock, dir_mock, *a):
            call    = mock.call
            subject = updater.GithubStrategy('owner/repo')
            subject.perform_update()

            new_files = file_mock.call_args_list
            new_dirs  = dir_mock.call_args_list
            def bp(*a):
                return Core.storage.join_path(Core.bundle_path, *a)

            # makes dirs
            ok_(call(bp('')) in new_dirs)
            ok_(call(bp('dir', '')) in new_dirs)

            # makes files
            ok_(call(bp('file'), '') in new_files)
            ok_(call(bp('dir', 'file'), '') in new_files)

            # skips hidden dirs
            ok_(call(bp('.hidden-dir', '')) not in new_dirs)

            # skips hidden files
            ok_(call(bp('.hidden'), '') not in new_files)
            ok_(call(bp('.hidden-dir', 'file'), '') not in new_files)

        test()
