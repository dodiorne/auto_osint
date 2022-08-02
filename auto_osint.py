#!/usr/bin/env python3

__version__ = '1.1.8'


from os import makedirs
from os.path import expanduser
import subprocess
import argparse
from getpass import getpass

# Output Definitions

company_name = 'CompanyName'
linkedin_company = 'company-name'
company_domain = 'company-name.com'

linkedin_username = 'john.doe@iflockconsulting.com'
linkedin_password = 'password123'

output_directory = expanduser('~/OSINT')

# This shouldn't affect anything because it only checks if the command is being ran anyways
skip_list = ['eyewitness']

# TODO: Need a way to link these to the tasks actually being ran in order to not make unneeded directories
def make_directories():
    dirs = [
        f'{output_directory}/{company_name}/Dehashed',
        f'{output_directory}/{company_name}/Gowitness',
        f'{output_directory}/{company_name}/Linkedin2Username',
        f'{output_directory}/{company_name}/MX Records',
        f'{output_directory}/{company_name}/PyMeta/pymeta-files',
        f'{output_directory}/{company_name}/Subdomains',
        f'{output_directory}/{company_name}/Whois',
    ]

    for name in dirs:
        print(f'Making directory: {name}')
        makedirs(name, exist_ok=True)

# TODO: These maybe should just be plain strings and be formatted later
def get_commands():
    commands = {
        'li2u': {
            'depends': [],
            'directory': f'{output_directory}/{company_name}/Linkedin2Username',
            'command': f'linkedin2username -c "{linkedin_company}" -u "{linkedin_username}" -p "{linkedin_password}" && mv ./li2u-output/* "./" && rm -r "./li2u-output" | tee "./{company_name}_li2u.out"',
        },
        'pymeta': {
            'depends': [],
            'directory': f'{output_directory}/{company_name}/PyMeta',
            'command': f'pymeta -d "{company_domain}" -f ".{company_name}_pymeta.csv" -o "./pymeta-files" | tee "./{company_name}_pymeta.out"',
        },
        'whois': {
            'depends': [],
            'directory': f'{output_directory}/{company_name}/Whois',
            'command': f'whois "{company_domain}" | tee "./{company_name}_whois.out"',
        },
        'mx_records': {
            'depends': [],
            'directory': f'{output_directory}/{company_name}/MX Records',
            'command': f'nslookup -type=mx "{company_domain}" 1.1.1.1 2> /dev/null | tee "./{company_name}_mx-records.out"',
        },
        'sublist3r': {
            'depends': [],
            'directory': f'{output_directory}/{company_name}/Subdomains',
            'command': f'sublist3r -d "{company_domain}" -o "./{company_name}_sublist3r.lst" | tee "./{company_name}_sublist3r.out"',
        },
        'crt_sh': {
            'depends': [],
            'directory': f'{output_directory}/{company_name}/Subdomains',
            'command': fr'curl --retry 5 -s "https://crt.sh/?q={company_domain}" | tee "./{company_name}_crt-sh.html" | tq "td:nth-child(5),td:nth-child(6)" | sed -r "s|</?\w+/?>|\n|g" | grep "{company_domain}" | grep -v "\*" | sort -u | tee "./{company_name}_crt-sh.lst"'
        },
        'gowitness': {
            'depends': ['crt_sh', 'sublist3r'],
            'directory': f'{output_directory}/{company_name}/Gowitness',
            'command': f'cat ../Subdomains/*.lst | sort -u | gowitness file -f - --delay 5 |& tee "./{company_name}_gowitness.out" | grep -v "ERROR"',
        },
        # 'eyewitness': {
        #    'depends': [],
        #    'directory': f'{output_directory}/{company_name}/Eyewitness',
        #    'command': f'eyewitness --web -f "../Subdomains/{company_name}_sublist3r.lst" -d "./eyewitness_{company_name}_login-forms" --no-prompt | tee "./{company_name}_eyewitness.out"',
        # },
    }

    return commands

# ask for linkedin creds
def linkedin_creds_prompt():
    global linkedin_username, linkedin_password

    linkedin_username = input('Linkedin Email: ')
    linkedin_password = getpass('Linkedin Password: ')

def run_command(name, directory, command, depends):
    global skip_list

    if any(x in skip_list for x in depends):
        print(f'Step "{name}" depends on {", ".join(depends)}; One or more of these were skipped\n')
        return

    print(f'Running step "{name}"...\n')

    print('$ {command}\n'.format(directory=directory, command=command.replace(linkedin_password, '***').replace(linkedin_username, '***')))
    # TODO: Make way for this to be ran without outputting everything to the console, just saving to file for later
    # TODO: This isn't good at handling errors (meaning it doesn't at all)
    subprocess.run(['bash', '-c', f'cd "{directory}" && {command}'])

    # TODO: Automate command parsing
    input('\n\nTake a screenshot now, then press ENTER ')
    print('')

# Command Parsing
def main():
    global company_name, company_domain, linkedin_company, skip_list

    # Parse Argument
    # TODO: Split these off into separate function
    parser = argparse.ArgumentParser(description='OSINT Tools Automation Script')
    parser.add_argument('--name', type=str, help='name of company (used for file output names)', required=True)
    parser.add_argument('--linkedin', type=str, help='linkedin company name (get from url)', required=True)
    parser.add_argument('--domain', type=str, help='domain name of company', required=True)
    parser.add_argument('--skip', type=str, help='any of pymeta, li2u, whois, mx_records, sublist3r, crt_sh, gowitness (comma separated)')
    # parser.add_argument('--only', type=str, help='one of pymeta, li2u, whois, mx_records, subdomains, gowitness')
    parser.add_argument('--version', action='version', version=f'OSINT Tools Automation Script v. {__version__}')

    args = parser.parse_args()

    company_name = args.name
    company_domain = args.domain
    linkedin_company = args.linkedin

    if args.skip is not None:
        skip_list.append(args.skip.split(','))

    # prompt for linkedin creds if not skipped
    if 'li2u' not in skip_list:
        linkedin_creds_prompt()

    make_directories()

    # Run Commands
    for name, cmd in get_commands().items():
        if name in skip_list:
            continue

        run_command(name, **cmd)


if __name__ == '__main__':
    main()
