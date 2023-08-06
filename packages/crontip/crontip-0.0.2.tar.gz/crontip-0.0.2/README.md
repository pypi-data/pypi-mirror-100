# Crontip
Crontip is a tool uesd for backup and install of crontab.

## Installation
You can install crontip by:
`pip install crontip`
*(please use latest pip to install)*

## Usage

### Backup the Current Crontab

1. backup into default destination

    `crontip -b` or `crontip --backup`

    will backup the current crontab and save it into the *backup_folder*.

2. appointe the destination with `-o`

    `crontip -b -o ./this_is_a_backup`

    save the backup into `./this_is_a_backup`


### Edit the Prepared Copy of Backup

`crontip -e` or `crontip --edit`



The editing process **automatically** through two steps:

1. copy the latest backup into ready folder
`cp backup/latest.bk ready/latest.bk`

2. open file with vim
`vim ready/latest.bk`
