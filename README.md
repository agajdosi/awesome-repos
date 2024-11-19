# Awesome Repos

A Blender add-on for seamless addition of third-party extension repositories into Blender.

Not all Blender add-ons (can) meet the official [extensions.blender.org](https://extensions.blender.org/terms-of-service/) requirements, often for valid reasons.
This add-on empowers users to freely and easily add alternative extension repositories.

## How to Contribute

### Adding a Repository
If you'd like to add your own or another useful Blender extension repository, please create an issue—or better yet, a pull request (PR)—that includes the desired extensions API endpoint. 

For an issue submission, include the following details:
- Repository name
- Repository owner
- Repository URL

All repositories must comply with the latest [API](http://extensions.blender.org/api/swagger/) and must absolutely not contain malicious code.

### Repository Removal
If you encounter malicious code in any of the listed repositories and the repository owner refuses to address or unlist it, please create an issue requesting the removal of the repository. 

While I do not actively monitor the repositories for malicious code, I take a strong stance against its spread.
If notified, I will promptly investigate and remove the affected repository as soon as possible.

### Developing
Even though this add-on can be built standardly with: `b --command extension build --output-dir ~` custom `dev.py` script is packed in the repository.

To build the add-on, please run:
`python3 build.py --install-at "<path-to-extensions/user_default>"`

E.g.:
`python3 build.py --install-at "/Users/username/Library/Application Support/Blender/4.3/extensions/user_default"`.

Add-on will be built in `./out/awesome-repos.zip`.
In `./out/awesome-repos/` you can see all the files of the .zip file directly.
The .zip file will be also copied into the `--install-at` location, so you do not need to install it manually and you can try it right away in the Blender.
