import urllib2
import os
import tarfile
import logging

class Release:
    """The path of this release."""
    path = None
    """The version of this release."""
    version = None

    _release_url = 'https://cgal.geometryfactory.com/CGAL/Members/Releases/'
    _latest_url = os.path.join(_release_url, 'LATEST')

    def __init__(self, testsuite, use_local, user, passwd):
        if not use_local and user and passwd:
            logging.info('Setting up user and password for download.')
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, Release._release_url, user, passwd)
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)

        if use_local:
            logging.info('Using local CGAL release at {}'.format(testsuite))
            self.path = testsuite
        else:
            logging.info('Trying to determine LATEST')
            latest = Release._get_latest()
            logging.info('LATEST is {}'.format(latest))
            path_to_tar = Release._get_cgal(latest, testsuite)
            logging.info('Extracting {}'.format(path_to_tar))
            self.path = Release._extract_release(path_to_tar)

        assert os.path.isdir(self.path), '{} is not a directory'.format(self.path)
        self.version = self._extract_version()

    def __str__(self):
        return self.path

    @staticmethod
    def _get_latest():
        try:
            response = urllib2.urlopen(Release._latest_url)
            return response.read().strip()
        except urllib2.URLError as e:
            if hasattr(e, 'code') and e.code == 401:
                print 'Did you forget to provide --user and --passwd?'
            sys.exit('Failure retrieving LATEST: ' +  e.reason)

    @staticmethod
    def _get_cgal(latest, testsuite):
        download_from=os.path.join(Release._release_url, latest)
        download_to=os.path.join(testsuite, os.path.basename(download_from))
        logging.info('Trying to download from {} to {}'.format(download_from, download_to))

        if os.path.exists(download_to):
            logging.warning('Path {} already exists, reusing it.'.format(download_to))
            return download_to

        try:
            response = urllib2.urlopen(download_from)
            with open(download_to, "wb") as local_file:
                local_file.write(response.read())
                return download_to
        except urllib2.URLError as e:
            if hasattr(e, 'code') and e.code == 401:
                print 'Did you forget to provide --user and --passwd?'
                sys.exit('Failure retrieving the CGAL specified by latest.' + e.reason)

    @staticmethod
    def _extract_release(path_to_release_tar):
        """Extract the CGAL release tar ball specified by `path_to_release_tar` into the
        directory of `path_to_release_tar`.  The tar ball can only contain a single
        directory, which cannot be an absolute path. Returns the path to
        the extracted directory."""
        assert tarfile.is_tarfile(path_to_release_tar), 'Path provided to extract is not a tarfile'
        tar = tarfile.open(path_to_release_tar)
        commonprefix = os.path.commonprefix(tar.getnames())
        assert commonprefix != '.', 'Tarfile has no single common prefix'
        assert not os.path.isabs(commonprefix), 'Common prefix is an absolute path'
        tar.extractall(os.path.dirname(path_to_release_tar)) # extract to the download path
        tar.close()
        return os.path.join(os.path.dirname(path_to_release_tar), commonprefix)

    def _extract_version(self):
        release_id = None
        try:
            version_file = os.path.join(self.path, 'VERSION')
            fp = open(version_file)
        except IOError:
            logging.warning('Could not read VERSION file {}'.format(version_file))
        else:
            with fp:
                release_id = fp.read().replace('\n', '')
        return release_id

if __name__ == "__main__":
    pass
