import re
import csv
import random
import sys
from tabulate import tabulate

POSITIONS = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']

def main():
    '''
        This program reads csv file and generates a team.
        Keys: Player, Position, Age, Skill.
        Gets the file name from the command line.
    '''
    if len(sys.argv[1:]) != 1 or not(sys.argv[1].endswith('.csv')):
        sys.exit('Only one argument with csv format file names are accepted.')
    try:
        players = read_file()
        formation = make_formation()
        sort_option = get_sort_option()
        team = build_team(players, formation, sort_option)
        output(team)
    except FileNotFoundError:
        print(f"File '{sys.argv[1]}' not found.")
    except ValueError as error_message:
        print(error_message)
    except EOFError:
        sys.exit('Program exit.')

def get_sort_option():
    '''
        Asks for valid sorting option
    '''
    while True:
        try:
            sort_by = input('Sort by? \n1 for by Skill \n2 for by Age \n3 for by random\nEnter: ')
            return validate_sort(sort_by)
        except ValueError:
            pass

def validate_sort(sort_by):
    '''
        Validate sorting input
        :param sort_by: Sorting options
        :type sort_by: str
        :raise ValueError: If sort_by is not 1, 2 or 3
        :return: 1. Skill 2. Age 3. Random
        :rtype: str
    '''
    match int(sort_by):
        case 1|2|3:
            return sort_by
        case _:
            raise ValueError('Invalid input')

def build_team(players, formation, sort_option):
    '''
        Builds up team.
        :param players: List of player dictionaries containing player data.
        :type players: list of dict
        :param formation: Formation to use for building a team. (e.g. '4-3-3')
        :type formation: str
        :param sort_option: Sorting option to use for selecting players: '1' for Skill, '2' for age, '3' for random.
        :type sort_option: str
        :return: A list of players sorted and assigned to positions based on the formation.
        :rtype: a list of dict
    '''
    team = []
    parsed_formation = parse(formation)
    age = None
    if int(sort_option) == 2:
        age = get_age()

    for player_num_in_position, position in zip(parsed_formation, POSITIONS):
        args = sort_option, [player for player in players if player['Position'] == f'{position}'], player_num_in_position

        if age is not None:
            args += (age,)
        team.extend(sorted_players(*args))
    return team

def sorted_players(*args):
    '''
        Returns sorted players based on sort option
        There are minimum of 3 parameters, max of 4 if sorted by age.
        :param sort_option: By what to sort
        :type sort_option: str
        :param players_in_current_position: list of players dictionary in current position
        :type players_in_current_position: list of dict
        :param player_num_in_position: player number in the current iteration position
        :type player_num_in_position: int
        :param age: Optional argument only added when sorted by age
        :type age: str
    '''
    sort_option, players_in_current_position, player_num_in_position, *age = args
    match int(sort_option):
        case 1:
            return skilled_players(players_in_current_position, player_num_in_position)
        case 2:
            return aged_players(players_in_current_position, player_num_in_position, age[0])
        case 3:
            return random_players(players_in_current_position, player_num_in_position)

def read_file():
    with open(f'{sys.argv[1]}') as file:
        reader = csv.DictReader(file)
        return list(reader)

def output(team):
    print(tabulate(team, headers="keys", tablefmt='grid'))

def parse(formation):
    parsed = [1]
    formation_args = list(map(int, formation.split('-')))
    if len(formation_args) > 3:
        orientation = int(get_orientation())
        if orientation == 1:
            defenders, midfielders, *forwards = formation_args
            parsed.extend([defenders, midfielders, sum(forwards)])
            return parsed
    defenders, *midfielders, forwards = formation_args
    parsed.extend([defenders, sum(midfielders), forwards])
    return parsed

def validate_orientation(orientation):
    match int(orientation):
        case 1|2:
            return orientation
        case _:
            raise ValueError()

def get_orientation():
    while True:
        try:
            orientation = input('1. Forward oriented 2. Midfielder oriented\nEnter: ')
            return validate_orientation(orientation)
        except ValueError:
            pass

def skilled_players(players_in_current_position, player_num):
    return sorted(players_in_current_position, key=lambda player:player['Skill'], reverse=True)[:player_num]

def aged_players(players_in_current_position, player_num, age):
    match int(age):
        case 1:
            return sorted(players_in_current_position, key=lambda player:player['Age'])[:player_num]
        case 2:
            return sorted(players_in_current_position, key=lambda player:player['Age'], reverse=True)[:player_num]

def random_players(players_in_current_position, player_num):
    return random.sample(players_in_current_position, k=player_num)

def get_age():
    while True:
        try:
            age = input('By young or old? \n1 for young \n2 for old\nEnter: ')
            return validate_age(age)
        except ValueError:
            pass
        except TypeError:
            pass

def validate_age(age):
    match int(age):
        case 1|2:
            return age
        case _:
            raise ValueError('Incorrect input')

def make_formation():
    formation = input('Formation: ')
    validate(formation)
    return formation

def validate(formation):
    '''
    Validation for formation.
    Checks total players, minimum defenders and input format (X-X-X[-X][-X]).
    '''
    check_format(formation)
    check_nums(formation)

def check_nums(formation):
    args = formation.split('-')
    if not valid_sum(args) or int(args[0]) < 3:
        raise ValueError("Invalid numbers: Total players must equal 10 or defenders must be at least 3.")

def check_format(formation):
    result = re.fullmatch(r'[1-5]-[1-5]-[1-5](-[1-5])?(-[1-5])?', formation)
    if not result:
        raise ValueError("Invalid format: Please use a format like X-X-X[-X][-X], where X is between 1 and 5.")

def valid_sum(args):
    return sum(map(int, args)) == 10

if __name__ == "__main__":
    main()
