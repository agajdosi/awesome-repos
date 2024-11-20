import argparse
import os
import shutil

ADDON_NAME = "awesome_repos"
OUT_DIR = "out"
IGNORE_PATTERNS = [
    os.path.basename(__file__), # do not include this file
    OUT_DIR, # do not include output directory
    ".gitignore",
    ".git",
    "*.md",
    ".DS_Store",
]


def do_build(install_at):
    print(f"Building {ADDON_NAME} addon...")
    src_dir = os.path.abspath(".")
    out_dir = os.path.abspath(OUT_DIR)
    addon_build_dir = os.path.join(out_dir, ADDON_NAME)
    shutil.rmtree(out_dir, ignore_errors=True)
    
    print("- copying files...")
    shutil.copytree( src_dir, addon_build_dir, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))

    print("- creating archive...")
    shutil.make_archive(addon_build_dir, "zip", out_dir, ADDON_NAME)
    
    if install_at is not None:
        install_at = os.path.join(install_at, ADDON_NAME)
        print(f"- copying to {install_at}...")
        shutil.rmtree(install_at, ignore_errors=True)
        shutil.copytree(addon_build_dir, install_at)

    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--install-at",
        type=str,
        default=None,
        help="If path is specified, then builded addon will be also copied to that location.",
    )
    args = parser.parse_args()
    do_build(args.install_at)
