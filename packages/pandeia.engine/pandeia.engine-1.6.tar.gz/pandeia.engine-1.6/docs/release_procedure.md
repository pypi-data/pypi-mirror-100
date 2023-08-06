0. Make sure the tagged release of pandeia_data does not have the hst/ or roman/ directories. (These should already have been removed during the release testing process)

1. Update the staging Pandeia Engine Installation pages
  - Get access via Brian Brooks or Bryan Holler
  - The filenames should be predictable: 
    - pip install pandeia.engine==X.Y.Z
    - https://stsci.box.com/v/pandeia-refdata-vXpYpZ

1. Generate and upload the data file
  - Create data tar file
      - Mark it as a release
      - Go to [pandeia_data](https://github.com/spacetelescope/pandeia_data), and click on the "Releases" link. Look for the latest release and download the source code (in tar.gz format).
  - Go to the folder you had downloaded the tar file located.
  - Upload that file to the ETC Project folder (create a new release folder if necessary) on box.stsci.edu
  - Set sharing to everyone with the link and use the Custom URL feature (in Link Settings) to set the name to pandeia-refdata-vXpYpZ.


2. Follow instruction [here](http://peterdowns.com/posts/first-time-with-pypi.html) to generate and upload the source code to the https://pypi.python.org/pypi/pandeia.engine
  - In section 'Create a .pypirc configuration file' if the .pypirc file does not exist.
  - In a fresh checkout of pandeia vX.Y.Z
    - `cd engine/`
    - Test creating an installation on test.pypi.org (you only have one shot at uploading to pypi for real - uploads cannot be edited or replaced.)
       - see ["Using TestPyPi"](https://packaging.python.org/guides/using-testpypi/) for instructions on using twine to upload to TestPyPi)
       - Edit the pypirc file to point to test.pypi.org
       - Create source distribution with `python setup.py sdist`; it should make a tar.gz file
       - Use twine to upload to testpypi
       - check test.pypi to make sure it uploaded correctly.

    - Generate source distribution and upload to pypi: `python setup.py sdist upload -r pypi`

3. Test
 - Go to https://pypi.python.org/pypi/pandeia.engine to see if the package is sucessfully uploaded.
 - Install a fresh version of the latest third party software and load that environment by typing `source /path/to/third/party pandeia_<third_party_version>`.
 - `pip freeze | grep pandeia.engine` (note the version, e.g. 1.2.1dev0)
 - `pip install pandeia.engine --upgrade`
 - test it by running the `pip freeze | grep pandeia.engine` command again and note the version should have changed (e.g. v1.3)
 - Follow the usage instruction in [pypi](https://pypi.python.org/pypi/pandeia.engine) to check if the users can follow the instruction as well.
 - Ask the engine dev to do a simple test and see if the new changes apply.

4. Notify
 - Notify Brian or Bryan that the JDOX page can be pushed to the public.
 - Update the Pandeia Engine News and Pandeia Engine Installation instructions
   https://outerspace.stsci.edu/display/PEN/Pandeia+Engine+News

--------------------

Making a Roman data release (on the assumption that running the engine for Roman requires only different data files):

1. Check out the release branch
2. Rewind the release branch to the commit before the hst and roman directories were removed with git reset --hard <commit>
3. Branch from that commit to vX.Y.Z_roman
4. Make a commit removing the jwst and hst directories
5. Make a `vX.Y.Z_roman` release
6. Download the resulting tarball and move it to a folder on the etc_project box
7. Make sure the file is shared to everyone with the link, and use the custom link feature (in Link Settings) to something like "pandeia-refdata-vXpYpZ-roman"
8. Update the Pandeia Engine News page and Pandeia Engine Installations outerspace page with the new download link.
https://outerspace.stsci.edu/display/PEN/Pandeia+Engine+News
9. Update the README and Docker installation files in Roman_tools with the new information (use the direct link Box offers from the Link Settings page in the Docker installation file)
