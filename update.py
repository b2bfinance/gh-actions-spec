#!/usr/bin/env go

# @todo: add more error handling, at this time, the operator should be able to
#   the read output to understand any errors produced.

import json
import tempfile
import http.client

"""Template for generated Go version.
"""
_TEMPLATE_GO_VERSION = """package schema

const Repository = ":repository"
const CommitSha = ":commit_sha"
"""


def get_latest_sha(repo) -> str:
    """Using the Github API get the lastest commit hash of the provided repo.
    """
    con = http.client.HTTPSConnection('api.github.com')
    con.request("GET", "https://api.github.com/repos/SchemaStore/schemastore/commits/master", headers={
        "user-agent": "github.com/b2bfinance/gh-actions-spec"
    })
    resp = con.getresponse()
    data = resp.read()
    resp.close()
    return json.loads(data)["sha"]


def get_file_contents(repo, sha, path):
    con = http.client.HTTPSConnection('raw.githubusercontent.com')
    con.request("GET", "https://raw.githubusercontent.com/{}/{}/{}".format(repo, sha, path), headers={
        "user-agent": "github.com/b2bfinance/gh-actions-spec"
    })
    resp = con.getresponse()
    data = resp.read()
    resp.close()
    return data


def write_temp_file(content) -> str:
    out_path = tempfile.mkstemp()[1]
    with open(out_path, "wb") as fout:
        fout.write(content)
    return out_path


def main(repo, spec_path, output_dir):
    """Get the latest commit hash of the Github repository provided. Then pull
    the JSON specification and store is temporarily, using it to generate the
    Go code that will be put into `output_dir`. Once this is done a file is
    added to the `output_dir` named `version.go` that will contain 2 constants
    `Repository` and `CommitSha`.
    """
    sha = get_latest_sha(repo)
    spec = get_file_contents(repo, sha, spec_path)
    local_spec_path = write_temp_file(spec)

    # todo: find a tool to generate the Go code using the specification.
    print(local_spec_path)


if __name__ == "__main__":
    main("SchemaStore/schemastore", "src/schemas/json/github-workflow.json", "./schema")
