import argparse
import json
import os
from datetime import datetime

# need to import requests and use to check wp-config / default dir and files / plugins directory

parser = argparse.ArgumentParser(description="WPwn - reviews wpscan output")
parser.add_argument("-f", "--file", required=True, help="copy your WPSCAN output to the working directory and supply "
                                                        "it using -f {file}.txt")
parser.add_argument("-u", "--url", required=True, help="add the target url. eg: -u cybercx.com.au")
args = parser.parse_args()
schema = {"toolname": "WPwn", "notes": "write that down", "scope": "Test", "issues": []}

search_terms = ["robots",
                "WordPress version",
                "XML-RPC",
                "wp-admin",
                "wp-cron",
                "WordPress theme",
                "directory has listing enabled",
                "User",
                "plugins"]


def triggered():
    for keyword in search_terms:
        output_file = f"{keyword}"
        scl(keyword, args.file, output_file)


def scl(search_term, input_file, output_file):
    if search_term == 'User':
        with open(input_file, 'r') as f_input, open(output_file, 'w') as f_output:
            found = False
            for line in f_input:
                if search_term in line:
                    found = True
                if found:
                    f_output.write(line)
    else:
        with open(input_file, 'r') as f_input, open(output_file, 'w') as f_output:
            found = False
            for line in f_input:
                if search_term in line:
                    found = True
                if found:
                    f_output.write(line)
                if not line.strip():  # empty line
                    found = False


def delete():  # searches directory and deletes files with no data to prevent false postive raise
    try:
        filenames = os.listdir('.')
        for filename in filenames:
            if os.path.isfile(filename) and os.path.getsize(filename) == 0:
                os.remove(filename)
                #  print(f"{filename} was not raised.")
    except OSError:
        print("Error reading directory contents.")


def sort():  # if filenames in dir match keywords in each case, raise finding - need to do more here.
    files = os.listdir('.')
    switch = {
        'robots': lambda: raisef(622, "via WPwn"),
        'Wordpress version': lambda: raisef(348, "via WPwn"),
        'directory has listing enabled': lambda: raisef(592, "via WPwn"),
        'XML-RPC': lambda: raisef(353, "via WPwn"),
        'wp-admin': lambda: raisef(355, "via WPwn"),
        'wp-Cron': lambda: raisef(349, "via WPwn"),
        'User': lambda: raisef(352, "via WPwn")
    }
    for file_name in files:
        if file_name in switch:
            switch[file_name]()
            print(file_name + " raised.")
    print("\n" + "a good consultant will manually verify these results ;) ")


def raisef(id, note):
    schema["issues"].append(
        {"finding_id": id, "consultant_note": note, "assets": args.url}
    )


def generate():
    now = datetime.now().strftime("%Y-%m-%d")
    with open(f"reportx_{now}.json", "w") as jsonFile:
        json.dump(schema, jsonFile)
        print(
            'JSON file generated. ReportX Word Tab > Finding > Import > Load > reportx.json to import.'
        )


def annoying():
    try:
        with open("common.txt", 'r') as common_terms, open("User", 'r') as usernames:
            file1 = set(word.lower() for word in common_terms.read().split())
            file2 = set(word.lower() for word in usernames.read().split())
            common_words = file1.intersection(file2)
            if common_words:
                print("Potentially guessable usernames enumerated: " + str(common_words))
                raisef(342, "Via WPwn")
    except FileNotFoundError:
        print("Issue checking for predictable usernames")


def main():
    triggered()  # takes search_terms list and checks scan input
    delete()  # removes false positive files from current directory
    sort()  # checks what files were generated and raises corresponding finding
    annoying()  # extra function to review username file for guessable names
    generate()  # generates .json import for reportx


if __name__ == "__main__":
    main()
