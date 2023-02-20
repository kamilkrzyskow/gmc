"""Script should be run before the tests before deployment to enable all plugins.

Not all plugins are required in the development stage, but even then MkDocs requires them to be installed.
Some developers might not have to test deployment plugins locally, so they're commented off by default.
This script replaces all comments in the `mkdocs.yml` file with their respective plugins.
This script also can turn the plugin entry back into comments.
"""
import sys


def main():

    mapping = {
        MINIFY_KEY: MINIFY_CONTENT,
        REVISION_DATE_KEY: REVISION_DATE_CONTENT,
        SOCIAL_KEY: SOCIAL_CONTENT,
    }

    key_count = 0
    content_count = 0

    with open("mkdocs.yml", encoding="utf8") as file:
        mkdocs = file.read()

    for key, content in mapping.items():
        key_count += mkdocs.count(key)
        content_count += mkdocs.count(content)

    try:
        assert ((key_count == len(mapping) and content_count == 0)
                or (content_count == len(mapping) and key_count == 0))
    except AssertionError:
        sys.exit(f"Error: Count isn't correct {key_count=}, {content_count=}")

    for key, content in mapping.items():
        if key_count > 0:
            mkdocs = mkdocs.replace(key, content)
        else:
            mkdocs = mkdocs.replace(content, key)

    with open("mkdocs.yml", "w", encoding="utf8") as file:
        file.write(mkdocs)

    if content_count > 0:
        sys.exit("Error: Swapped content with keys")

    print("Swapped keys with content")


MINIFY_KEY = "# MINIFY_PLUGIN"
MINIFY_CONTENT = """  - minify:
      minify_html: !ENV [GMC_ENABLE_ON_PUBLISH, False]
      minify_css: !ENV [GMC_ENABLE_ON_PUBLISH, False]
      minify_js: !ENV [GMC_ENABLE_ON_PUBLISH, False]
      cache_safe: !ENV [GMC_ENABLE_ON_PUBLISH, False]
      htmlmin_opts:
        remove_comments: true
      css_files:
        - assets/stylesheets/extra.css
      js_files:
        - assets/javascripts/extra.js"""

REVISION_DATE_KEY = "# REVISION_DATE_PLUGIN"
REVISION_DATE_CONTENT = """  - git-revision-date-localized:
      enabled: !ENV [GMC_ENABLE_ON_PUBLISH, False]
      type: iso_datetime
      timezone: Europe/Warsaw
      exclude:
        - index*.md
        - genome/index*.md
        - zengin/index*.md"""

SOCIAL_KEY = "# SOCIAL_PLUGIN"
SOCIAL_CONTENT = """  - social:
      cards: !ENV [GMC_ENABLE_ON_PUBLISH, False]"""

if __name__ == '__main__':
    main()
